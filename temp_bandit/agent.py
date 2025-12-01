@@ -1,44 +1,50 @@
-import os
 import shutil
 import subprocess
-from typing import Any, Dict, List, Literal, Optional, Union
+from typing import Any, Dict, List, Literal, Optional, Sequence, Type, Union
 
 from pydantic import Field, InstanceOf, PrivateAttr, model_validator
 
 from crewai.agents import CacheHandler
 from crewai.agents.agent_builder.base_agent import BaseAgent
 from crewai.agents.crew_agent_executor import CrewAgentExecutor
-from crewai.cli.constants import ENV_VARS, LITELLM_PARAMS
 from crewai.knowledge.knowledge import Knowledge
 from crewai.knowledge.source.base_knowledge_source import BaseKnowledgeSource
 from crewai.knowledge.utils.knowledge_utils import extract_knowledge_context
-from crewai.llm import LLM
+from crewai.lite_agent import LiteAgent, LiteAgentOutput
+from crewai.llm import BaseLLM
 from crewai.memory.contextual.contextual_memory import ContextualMemory
+from crewai.security import Fingerprint
 from crewai.task import Task
 from crewai.tools import BaseTool
 from crewai.tools.agent_tools.agent_tools import AgentTools
-from crewai.tools.base_tool import Tool
 from crewai.utilities import Converter, Prompts
+from crewai.utilities.agent_utils import (
+    get_tool_names,
+    load_agent_from_repository,
+    parse_tools,
+    render_text_description_and_args,
+)
 from crewai.utilities.constants import TRAINED_AGENTS_DATA_FILE, TRAINING_DATA_FILE
 from crewai.utilities.converter import generate_model_description
+from crewai.utilities.events.agent_events import (
+    AgentExecutionCompletedEvent,
+    AgentExecutionErrorEvent,
+    AgentExecutionStartedEvent,
+)
+from crewai.utilities.events.crewai_event_bus import crewai_event_bus
+from crewai.utilities.events.knowledge_events import (
+    KnowledgeQueryCompletedEvent,
+    KnowledgeQueryFailedEvent,
+    KnowledgeQueryStartedEvent,
+    KnowledgeRetrievalCompletedEvent,
+    KnowledgeRetrievalStartedEvent,
+    KnowledgeSearchQueryFailedEvent,
+)
+from crewai.utilities.llm_utils import create_llm
 from crewai.utilities.token_counter_callback import TokenCalcHandler
 from crewai.utilities.training_handler import CrewTrainingHandler
 
-agentops = None
 
-try:
-    import agentops  # type: ignore # Name ""agentops"" is already defined
-    from agentops import track_agent  # type: ignore
-except ImportError:
-
-    def track_agent():
-        def noop(f):
-            return f
-
-        return noop
-
-
-@track_agent()
 class Agent(BaseAgent):
     """"""Represents an agent in a system.
 
@@ -55,13 +61,13 @@ class Agent(BaseAgent):
             llm: The language model that will run the agent.
             function_calling_llm: The language model that will handle the tool calling for this agent, it overrides the crew function_calling_llm.
             max_iter: Maximum number of iterations for an agent to execute a task.
-            memory: Whether the agent should have memory or not.
             max_rpm: Maximum number of requests per minute for the agent execution to be respected.
             verbose: Whether the agent execution should be in verbose mode.
             allow_delegation: Whether the agent is allowed to delegate tasks to other agents.
             tools: Tools at agents disposal
             step_callback: Callback to be executed after each step of the agent execution.
             knowledge_sources: Knowledge sources for the agent.
+            embedder: Embedder configuration for the agent.
     """"""
 
     _times_executed: int = PrivateAttr(default=0)
@@ -71,9 +77,6 @@ class Agent(BaseAgent):
     )
     agent_ops_agent_name: str = None  # type: ignore # Incompatible types in assignment (expression has type ""None"", variable has type ""str"")
     agent_ops_agent_id: str = None  # type: ignore # Incompatible types in assignment (expression has type ""None"", variable has type ""str"")
-    cache_handler: InstanceOf[CacheHandler] = Field(
-        default=None, description=""An instance of the CacheHandler class.""
-    )
     step_callback: Optional[Any] = Field(
         default=None,
         description=""Callback to be executed after each step of the agent execution."",
@@ -82,10 +85,10 @@ class Agent(BaseAgent):
         default=True,
         description=""Use system prompt for the agent."",
     )
-    llm: Union[str, InstanceOf[LLM], Any] = Field(
+    llm: Union[str, InstanceOf[BaseLLM], Any] = Field(
         description=""Language model that will run the agent."", default=None
     )
-    function_calling_llm: Optional[Any] = Field(
+    function_calling_llm: Optional[Union[str, InstanceOf[BaseLLM], Any]] = Field(
         description=""Language model that will run the agent."", default=None
     )
     system_template: Optional[str] = Field(
@@ -97,20 +100,13 @@ class Agent(BaseAgent):
     response_template: Optional[str] = Field(
         default=None, description=""Response format for the agent.""
     )
-    tools_results: Optional[List[Any]] = Field(
-        default=[], description=""Results of the tools used by the agent.""
-    )
     allow_code_execution: Optional[bool] = Field(
         default=False, description=""Enable code execution for the agent.""
     )
     respect_context_window: bool = Field(
         default=True,
         description=""Keep messages under the context window size by summarizing content."",
     )
-    max_iter: int = Field(
-        default=20,
-        description=""Maximum number of iterations for an agent to execute a task before giving it's best answer"",
-    )
     max_retry_limit: int = Field(
         default=2,
         description=""Maximum number of retries for an agent to execute a task when an error occurs."",
@@ -131,105 +127,42 @@ class Agent(BaseAgent):
         default=None,
         description=""Maximum number of reasoning attempts before executing the task. If None, will try until ready."",
     )
-    embedder_config: Optional[Dict[str, Any]] = Field(
+    embedder: Optional[Dict[str, Any]] = Field(
         default=None,
         description=""Embedder configuration for the agent."",
     )
-    knowledge_sources: Optional[List[BaseKnowledgeSource]] = Field(
+    agent_knowledge_context: Optional[str] = Field(
+        default=None,
+        description=""Knowledge context for the agent."",
+    )
+    crew_knowledge_context: Optional[str] = Field(
+        default=None,
+        description=""Knowledge context for the crew."",
+    )
+    knowledge_search_query: Optional[str] = Field(
         default=None,
-        description=""Knowledge sources for the agent."",
+        description=""Knowledge search query for the agent dynamically generated by the agent."",
     )
-    _knowledge: Optional[Knowledge] = PrivateAttr(
+    from_repository: Optional[str] = Field(
         default=None,
+        description=""The Agent's role to be used from your repository."",
     )
 
+    @model_validator(mode=""before"")
+    def validate_from_repository(cls, v):
+        if v is not None and (from_repository := v.get(""from_repository"")):
+            return load_agent_from_repository(from_repository) | v
+        return v
+
     @model_validator(mode=""after"")
     def post_init_setup(self):
-        self._set_knowledge()
         self.agent_ops_agent_name = self.role
-        unaccepted_attributes = [
-            ""AWS_ACCESS_KEY_ID"",
-            ""AWS_SECRET_ACCESS_KEY"",
-            ""AWS_REGION_NAME"",
-        ]
-
-        # Handle different cases for self.llm
-        if isinstance(self.llm, str):
-            # If it's a string, create an LLM instance
-            self.llm = LLM(model=self.llm)
-        elif isinstance(self.llm, LLM):
-            # If it's already an LLM instance, keep it as is
-            pass
-        elif self.llm is None:
-            # Determine the model name from environment variables or use default
-            model_name = (
-                os.environ.get(""OPENAI_MODEL_NAME"")
-                or os.environ.get(""MODEL"")
-                or ""gpt-4o-mini""
-            )
-            llm_params = {""model"": model_name}
 
-            api_base = os.environ.get(""OPENAI_API_BASE"") or os.environ.get(
-                ""OPENAI_BASE_URL""
-            )
-            if api_base:
-                llm_params[""base_url""] = api_base
-
-            set_provider = model_name.split(""/"")[0] if ""/"" in model_name else ""openai""
-
-            # Iterate over all environment variables to find matching API keys or use defaults
-            for provider, env_vars in ENV_VARS.items():
-                if provider == set_provider:
-                    for env_var in env_vars:
-                        # Check if the environment variable is set
-                        key_name = env_var.get(""key_name"")
-                        if key_name and key_name not in unaccepted_attributes:
-                            env_value = os.environ.get(key_name)
-                            if env_value:
-                                key_name = key_name.lower()
-                                for pattern in LITELLM_PARAMS:
-                                    if pattern in key_name:
-                                        key_name = pattern
-                                        break
-                                llm_params[key_name] = env_value
-                        # Check for default values if the environment variable is not set
-                        elif env_var.get(""default"", False):
-                            for key, value in env_var.items():
-                                if key not in [""prompt"", ""key_name"", ""default""]:
-                                    # Only add default if the key is already set in os.environ
-                                    if key in os.environ:
-                                        llm_params[key] = value
-
-            self.llm = LLM(**llm_params)
-        else:
-            # For any other type, attempt to extract relevant attributes
-            llm_params = {
-                ""model"": getattr(self.llm, ""model_name"", None)
-                or getattr(self.llm, ""deployment_name"", None)
-                or str(self.llm),
-                ""temperature"": getattr(self.llm, ""temperature"", None),
-                ""max_tokens"": getattr(self.llm, ""max_tokens"", None),
-                ""logprobs"": getattr(self.llm, ""logprobs"", None),
-                ""timeout"": getattr(self.llm, ""timeout"", None),
-                ""max_retries"": getattr(self.llm, ""max_retries"", None),
-                ""api_key"": getattr(self.llm, ""api_key"", None),
-                ""base_url"": getattr(self.llm, ""base_url"", None),
-                ""organization"": getattr(self.llm, ""organization"", None),
-            }
-            # Remove None values to avoid passing unnecessary parameters
-            llm_params = {k: v for k, v in llm_params.items() if v is not None}
-            self.llm = LLM(**llm_params)
-
-        # Similar handling for function_calling_llm
-        if self.function_calling_llm:
-            if isinstance(self.function_calling_llm, str):
-                self.function_calling_llm = LLM(model=self.function_calling_llm)
-            elif not isinstance(self.function_calling_llm, LLM):
-                self.function_calling_llm = LLM(
-                    model=getattr(self.function_calling_llm, ""model_name"", None)
-                    or getattr(self.function_calling_llm, ""deployment_name"", None)
-                    or str(self.function_calling_llm)
-                )
+        self.llm = create_llm(self.llm)
+        if self.function_calling_llm and not isinstance(
+            self.function_calling_llm, BaseLLM
+        ):
+            self.function_calling_llm = create_llm(self.function_calling_llm)
 
         if not self.agent_executor:
             self._setup_agent_executor()
@@ -244,21 +177,41 @@ def _setup_agent_executor(self):
             self.cache_handler = CacheHandler()
         self.set_cache_handler(self.cache_handler)
 
-    def _set_knowledge(self):
+    def set_knowledge(self, crew_embedder: Optional[Dict[str, Any]] = None):
         try:
+            if self.embedder is None and crew_embedder:
+                self.embedder = crew_embedder
+
             if self.knowledge_sources:
-                knowledge_agent_name = f""{self.role.replace(' ', '_')}""
                 if isinstance(self.knowledge_sources, list) and all(
                     isinstance(k, BaseKnowledgeSource) for k in self.knowledge_sources
                 ):
-                    self._knowledge = Knowledge(
+                    self.knowledge = Knowledge(
                         sources=self.knowledge_sources,
-                        embedder_config=self.embedder_config,
-                        collection_name=knowledge_agent_name,
+                        embedder=self.embedder,
+                        collection_name=self.role,
+                        storage=self.knowledge_storage or None,
                     )
         except (TypeError, ValueError) as e:
             raise ValueError(f""Invalid Knowledge Configuration: {str(e)}"")
 
+    def _is_any_available_memory(self) -> bool:
+        """"""Check if any memory is available.""""""
+        if not self.crew:
+            return False
+
+        memory_attributes = [
+            ""memory"",
+            ""memory_config"",
+            ""_short_term_memory"",
+            ""_long_term_memory"",
+            ""_entity_memory"",
+            ""_user_memory"",
+            ""_external_memory"",
+        ]
+
+        return any(getattr(self.crew, attr) for attr in memory_attributes)
+
     def execute_task(
         self,
         task: Task,
@@ -274,6 +227,11 @@ def execute_task(
 
         Returns:
             Output of the agent
+
+        Raises:
+            TimeoutError: If execution exceeds the maximum execution time.
+            ValueError: If the max execution time is not a positive integer.
+            RuntimeError: If the agent execution fails for other reasons.
         """"""
         if self.reasoning:
             try:
@@ -303,46 +261,95 @@ def execute_task(
             if task.output_json:
                 # schema = json.dumps(task.output_json, indent=2)
                 schema = generate_model_description(task.output_json)
+                task_prompt += ""
"" + self.i18n.slice(
+                    ""formatted_task_instructions""
+                ).format(output_format=schema)
 
             elif task.output_pydantic:
                 schema = generate_model_description(task.output_pydantic)
-
-            task_prompt += ""
"" + self.i18n.slice(""formatted_task_instructions"").format(
-                output_format=schema
-            )
+                task_prompt += ""
"" + self.i18n.slice(
+                    ""formatted_task_instructions""
+                ).format(output_format=schema)
 
         if context:
             task_prompt = self.i18n.slice(""task_with_context"").format(
                 task=task_prompt, context=context
             )
 
-        if self.crew and self.crew.memory:
+        if self._is_any_available_memory():
             contextual_memory = ContextualMemory(
                 self.crew.memory_config,
                 self.crew._short_term_memory,
                 self.crew._long_term_memory,
                 self.crew._entity_memory,
                 self.crew._user_memory,
+                self.crew._external_memory,
             )
             memory = contextual_memory.build_context_for_task(task, context)
             if memory.strip() != """":
                 task_prompt += self.i18n.slice(""memory"").format(memory=memory)
+        knowledge_config = (
+            self.knowledge_config.model_dump() if self.knowledge_config else {}
+        )
 
-        if self._knowledge:
-            agent_knowledge_snippets = self._knowledge.query([task.prompt()])
-            if agent_knowledge_snippets:
-                agent_knowledge_context = extract_knowledge_context(
-                    agent_knowledge_snippets
+        if self.knowledge:
+            crewai_event_bus.emit(
+                self,
+                event=KnowledgeRetrievalStartedEvent(
+                    agent=self,
+                ),
+            )
+            try:
+                self.knowledge_search_query = self._get_knowledge_search_query(
+                    task_prompt
+                )
+                if self.knowledge_search_query:
+                    agent_knowledge_snippets = self.knowledge.query(
+                        [self.knowledge_search_query], **knowledge_config
+                    )
+                    if agent_knowledge_snippets:
+                        self.agent_knowledge_context = extract_knowledge_context(
+                            agent_knowledge_snippets
+                        )
+                        if self.agent_knowledge_context:
+                            task_prompt += self.agent_knowledge_context
+                    if self.crew:
+                        knowledge_snippets = self.crew.query_knowledge(
+                            [self.knowledge_search_query], **knowledge_config
+                        )
+                        if knowledge_snippets:
+                            self.crew_knowledge_context = extract_knowledge_context(
+                                knowledge_snippets
+                            )
+                            if self.crew_knowledge_context:
+                                task_prompt += self.crew_knowledge_context
+
+                    crewai_event_bus.emit(
+                        self,
+                        event=KnowledgeRetrievalCompletedEvent(
+                            query=self.knowledge_search_query,
+                            agent=self,
+                            retrieved_knowledge=(
+                                (self.agent_knowledge_context or """")
+                                + (
+                                    ""
""
+                                    if self.agent_knowledge_context
+                                    and self.crew_knowledge_context
+                                    else """"
+                                )
+                                + (self.crew_knowledge_context or """")
+                            ),
+                        ),
+                    )
+            except Exception as e:
+                crewai_event_bus.emit(
+                    self,
+                    event=KnowledgeSearchQueryFailedEvent(
+                        query=self.knowledge_search_query or """",
+                        agent=self,
+                        error=str(e),
+                    ),
                 )
-                if agent_knowledge_context:
-                    task_prompt += agent_knowledge_context
-
-        if self.crew:
-            knowledge_snippets = self.crew.query_knowledge([task.prompt()])
-            if knowledge_snippets:
-                crew_knowledge_context = extract_knowledge_context(knowledge_snippets)
-                if crew_knowledge_context:
-                    task_prompt += crew_knowledge_context
 
         tools = tools or self.tools or []
         self.create_agent_executor(tools=tools, task=task)
@@ -353,17 +360,64 @@ def execute_task(
             task_prompt = self._use_trained_data(task_prompt=task_prompt)
 
         try:
-            result = self.agent_executor.invoke(
-                {
-                    ""input"": task_prompt,
-                    ""tool_names"": self.agent_executor.tools_names,
-                    ""tools"": self.agent_executor.tools_description,
-                    ""ask_for_human_input"": task.human_input,
-                }
-            )[""output""]
+            crewai_event_bus.emit(
+                self,
+                event=AgentExecutionStartedEvent(
+                    agent=self,
+                    tools=self.tools,
+                    task_prompt=task_prompt,
+                    task=task,
+                ),
+            )
+
+            # Determine execution method based on timeout setting
+            if self.max_execution_time is not None:
+                if (
+                    not isinstance(self.max_execution_time, int)
+                    or self.max_execution_time <= 0
+                ):
+                    raise ValueError(
+                        ""Max Execution time must be a positive integer greater than zero""
+                    )
+                result = self._execute_with_timeout(
+                    task_prompt, task, self.max_execution_time
+                )
+            else:
+                result = self._execute_without_timeout(task_prompt, task)
+
+        except TimeoutError as e:
+            # Propagate TimeoutError without retry
+            crewai_event_bus.emit(
+                self,
+                event=AgentExecutionErrorEvent(
+                    agent=self,
+                    task=task,
+                    error=str(e),
+                ),
+            )
+            raise e
         except Exception as e:
+            if e.__class__.__module__.startswith(""litellm""):
+                # Do not retry on litellm errors
+                crewai_event_bus.emit(
+                    self,
+                    event=AgentExecutionErrorEvent(
+                        agent=self,
+                        task=task,
+                        error=str(e),
+                    ),
+                )
+                raise e
             self._times_executed += 1
             if self._times_executed > self.max_retry_limit:
+                crewai_event_bus.emit(
+                    self,
+                    event=AgentExecutionErrorEvent(
+                        agent=self,
+                        task=task,
+                        error=str(e),
+                    ),
+                )
                 raise e
             result = self.execute_task(task, context, tools)
 
@@ -376,9 +430,64 @@ def execute_task(
         for tool_result in self.tools_results:  # type: ignore # Item ""None"" of ""list[Any] | None"" has no attribute ""__iter__"" (not iterable)
             if tool_result.get(""result_as_answer"", False):
                 result = tool_result[""result""]
-
+        crewai_event_bus.emit(
+            self,
+            event=AgentExecutionCompletedEvent(agent=self, task=task, output=result),
+        )
         return result
 
+    def _execute_with_timeout(self, task_prompt: str, task: Task, timeout: int) -> str:
+        """"""Execute a task with a timeout.
+
+        Args:
+            task_prompt: The prompt to send to the agent.
+            task: The task being executed.
+            timeout: Maximum execution time in seconds.
+
+        Returns:
+            The output of the agent.
+
+        Raises:
+            TimeoutError: If execution exceeds the timeout.
+            RuntimeError: If execution fails for other reasons.
+        """"""
+        import concurrent.futures
+
+        with concurrent.futures.ThreadPoolExecutor() as executor:
+            future = executor.submit(
+                self._execute_without_timeout, task_prompt=task_prompt, task=task
+            )
+
+            try:
+                return future.result(timeout=timeout)
+            except concurrent.futures.TimeoutError:
+                future.cancel()
+                raise TimeoutError(
+                    f""Task '{task.description}' execution timed out after {timeout} seconds. Consider increasing max_execution_time or optimizing the task.""
+                )
+            except Exception as e:
+                future.cancel()
+                raise RuntimeError(f""Task execution failed: {str(e)}"")
+
+    def _execute_without_timeout(self, task_prompt: str, task: Task) -> str:
+        """"""Execute a task without a timeout.
+
+        Args:
+            task_prompt: The prompt to send to the agent.
+            task: The task being executed.
+
+        Returns:
+            The output of the agent.
+        """"""
+        return self.agent_executor.invoke(
+            {
+                ""input"": task_prompt,
+                ""tool_names"": self.agent_executor.tools_names,
+                ""tools"": self.agent_executor.tools_description,
+                ""ask_for_human_input"": task.human_input,
+            }
+        )[""output""]
+
     def create_agent_executor(
         self, tools: Optional[List[BaseTool]] = None, task=None
     ) -> None:
@@ -387,12 +496,12 @@ def create_agent_executor(
         Returns:
             An instance of the CrewAgentExecutor class.
         """"""
-        tools = tools or self.tools or []
-        parsed_tools = self._parse_tools(tools)
+        raw_tools: List[BaseTool] = tools or self.tools or []
+        parsed_tools = parse_tools(raw_tools)
 
         prompt = Prompts(
             agent=self,
-            tools=tools,
+            has_tools=len(raw_tools) > 0,
             i18n=self.i18n,
             use_system_prompt=self.use_system_prompt,
             system_template=self.system_template,
@@ -414,12 +523,12 @@ def create_agent_executor(
             crew=self.crew,
             tools=parsed_tools,
             prompt=prompt,
-            original_tools=tools,
+            original_tools=raw_tools,
             stop_words=stop_words,
             max_iter=self.max_iter,
             tools_handler=self.tools_handler,
-            tools_names=self.__tools_names(parsed_tools),
-            tools_description=self._render_text_description_and_args(parsed_tools),
+            tools_names=get_tool_names(parsed_tools),
+            tools_description=render_text_description_and_args(parsed_tools),
             step_callback=self.step_callback,
             function_calling_llm=self.function_calling_llm,
             respect_context_window=self.respect_context_window,
@@ -434,13 +543,14 @@ def get_delegation_tools(self, agents: List[BaseAgent]):
         tools = agent_tools.tools()
         return tools
 
-    def get_multimodal_tools(self) -> List[Tool]:
+    def get_multimodal_tools(self) -> Sequence[BaseTool]:
         from crewai.tools.agent_tools.add_image_tool import AddImageTool
+
         return [AddImageTool()]
 
     def get_code_execution_tools(self):
         try:
-            from crewai_tools import CodeInterpreterTool
+            from crewai_tools import CodeInterpreterTool  # type: ignore
 
             # Set the unsafe_mode based on the code_execution_mode attribute
             unsafe_mode = self.code_execution_mode == ""unsafe""
@@ -453,25 +563,6 @@ def get_code_execution_tools(self):
     def get_output_converter(self, llm, text, model, instructions):
         return Converter(llm=llm, text=text, model=model, instructions=instructions)
 
-    def _parse_tools(self, tools: List[Any]) -> List[Any]:  # type: ignore
-        """"""Parse tools to be used for the task.""""""
-        tools_list = []
-        try:
-            # tentatively try to import from crewai_tools import BaseTool as CrewAITool
-            from crewai.tools import BaseTool as CrewAITool
-
-            for tool in tools:
-                if isinstance(tool, CrewAITool):
-                    tools_list.append(tool.to_structured_tool())
-                else:
-                    tools_list.append(tool)
-        except ModuleNotFoundError:
-            tools_list = []
-            for tool in tools:
-                tools_list.append(tool)
-
-        return tools_list
-
     def _training_handler(self, task_prompt: str) -> str:
         """"""Handle training data for the agent task prompt to improve output on Training.""""""
         if data := CrewTrainingHandler(TRAINING_DATA_FILE).load():
@@ -517,23 +608,6 @@ def _render_text_description(self, tools: List[Any]) -> str:
 
         return description
 
-    def _render_text_description_and_args(self, tools: List[BaseTool]) -> str:
-        """"""Render the tool name, description, and args in plain text.
-
-            Output will be in the format of:
-
-            .. code-block:: markdown
-
-            search: This tool is used for search, args: {""query"": {""type"": ""string""}}
-            calculator: This tool is used for math, \
-            args: {""expression"": {""type"": ""string""}}
-        """"""
-        tool_strings = []
-        for tool in tools:
-            tool_strings.append(tool.description)
-
-        return ""
"".join(tool_strings)
-
     def _validate_docker_installation(self) -> None:
         """"""Check if Docker is installed and running.""""""
         if not shutil.which(""docker""):
@@ -553,9 +627,146 @@ def _validate_docker_installation(self) -> None:
                 f""Docker is not running. Please start Docker to use code execution with agent: {self.role}""
             )
 
-    @staticmethod
-    def __tools_names(tools) -> str:
-        return "", "".join([t.name for t in tools])
-
     def __repr__(self):
         return f""Agent(role={self.role}, goal={self.goal}, backstory={self.backstory})""
+
+    @property
+    def fingerprint(self) -> Fingerprint:
+        """"""
+        Get the agent's fingerprint.
+
+        Returns:
+            Fingerprint: The agent's fingerprint
+        """"""
+        return self.security_config.fingerprint
+
+    def set_fingerprint(self, fingerprint: Fingerprint):
+        self.security_config.fingerprint = fingerprint
+
+    def _get_knowledge_search_query(self, task_prompt: str) -> str | None:
+        """"""Generate a search query for the knowledge base based on the task description.""""""
+        crewai_event_bus.emit(
+            self,
+            event=KnowledgeQueryStartedEvent(
+                task_prompt=task_prompt,
+                agent=self,
+            ),
+        )
+        query = self.i18n.slice(""knowledge_search_query"").format(
+            task_prompt=task_prompt
+        )
+        rewriter_prompt = self.i18n.slice(""knowledge_search_query_system_prompt"")
+        if not isinstance(self.llm, BaseLLM):
+            self._logger.log(
+                ""warning"",
+                f""Knowledge search query failed: LLM for agent '{self.role}' is not an instance of BaseLLM"",
+            )
+            crewai_event_bus.emit(
+                self,
+                event=KnowledgeQueryFailedEvent(
+                    agent=self,
+                    error=""LLM is not compatible with knowledge search queries"",
+                ),
+            )
+            return None
+
+        try:
+            rewritten_query = self.llm.call(
+                [
+                    {
+                        ""role"": ""system"",
+                        ""content"": rewriter_prompt,
+                    },
+                    {""role"": ""user"", ""content"": query},
+                ]
+            )
+            crewai_event_bus.emit(
+                self,
+                event=KnowledgeQueryCompletedEvent(
+                    query=query,
+                    agent=self,
+                ),
+            )
+            return rewritten_query
+        except Exception as e:
+            crewai_event_bus.emit(
+                self,
+                event=KnowledgeQueryFailedEvent(
+                    agent=self,
+                    error=str(e),
+                ),
+            )
+            return None
+
+    def kickoff(
+        self,
+        messages: Union[str, List[Dict[str, str]]],
+        response_format: Optional[Type[Any]] = None,
+    ) -> LiteAgentOutput:
+        """"""
+        Execute the agent with the given messages using a LiteAgent instance.
+
+        This method is useful when you want to use the Agent configuration but
+        with the simpler and more direct execution flow of LiteAgent.
+
+        Args:
+            messages: Either a string query or a list of message dictionaries.
+                     If a string is provided, it will be converted to a user message.
+                     If a list is provided, each dict should have 'role' and 'content' keys.
+            response_format: Optional Pydantic model for structured output.
+
+        Returns:
+            LiteAgentOutput: The result of the agent execution.
+        """"""
+        lite_agent = LiteAgent(
+            role=self.role,
+            goal=self.goal,
+            backstory=self.backstory,
+            llm=self.llm,
+            tools=self.tools or [],
+            max_iterations=self.max_iter,
+            max_execution_time=self.max_execution_time,
+            respect_context_window=self.respect_context_window,
+            verbose=self.verbose,
+            response_format=response_format,
+            i18n=self.i18n,
+            original_agent=self,
+        )
+
+        return lite_agent.kickoff(messages)
+
+    async def kickoff_async(
+        self,
+        messages: Union[str, List[Dict[str, str]]],
+        response_format: Optional[Type[Any]] = None,
+    ) -> LiteAgentOutput:
+        """"""
+        Execute the agent asynchronously with the given messages using a LiteAgent instance.
+
+        This is the async version of the kickoff method.
+
+        Args:
+            messages: Either a string query or a list of message dictionaries.
+                     If a string is provided, it will be converted to a user message.
+                     If a list is provided, each dict should have 'role' and 'content' keys.
+            response_format: Optional Pydantic model for structured output.
+
+        Returns:
+            LiteAgentOutput: The result of the agent execution.
+        """"""
+        lite_agent = LiteAgent(
+            role=self.role,
+            goal=self.goal,
+            backstory=self.backstory,
+            llm=self.llm,
+            tools=self.tools or [],
+            max_iterations=self.max_iter,
+            max_execution_time=self.max_execution_time,
+            respect_context_window=self.respect_context_window,
+            verbose=self.verbose,
+            response_format=response_format,
+            i18n=self.i18n,
+            original_agent=self,
+        )
+
+        return await lite_agent.kickoff_async(messages)