@@ -15,7 +15,8 @@
 
 from termcolor import colored
 
-import autogen
+from .... import AssistantAgent, ConversableAgent, OpenAIWrapper, UserProxyAgent, config_list_from_json
+from ....code_utils import CODE_BLOCK_PATTERN
 
 __all__ = [""AgentBuilder""]
 
@@ -37,7 +38,7 @@ def _config_check(config: dict):
 
 
 def _retrieve_json(text):
-    match = re.findall(autogen.code_utils.CODE_BLOCK_PATTERN, text, flags=re.DOTALL)
+    match = re.findall(CODE_BLOCK_PATTERN, text, flags=re.DOTALL)
     if not match:
         return text
     code_blocks = []
@@ -203,15 +204,15 @@ def __init__(
             builder_filter_dict.update({""model"": builder_model})
         if len(builder_model_tags) != 0:
             builder_filter_dict.update({""tags"": builder_model_tags})
-        builder_config_list = autogen.config_list_from_json(
+        builder_config_list = config_list_from_json(
             config_file_or_env, file_location=config_file_location, filter_dict=builder_filter_dict
         )
         if len(builder_config_list) == 0:
             raise RuntimeError(
                 f""Fail to initialize build manager: {builder_model}{builder_model_tags} does not exist in {config_file_or_env}. ""
                 f'If you want to change this model, please specify the ""builder_model"" in the constructor.'
             )
-        self.builder_model = autogen.OpenAIWrapper(config_list=builder_config_list)
+        self.builder_model = OpenAIWrapper(config_list=builder_config_list)
 
         self.agent_model = agent_model if isinstance(agent_model, list) else [agent_model]
         self.agent_model_tags = agent_model_tags
@@ -222,7 +223,7 @@ def __init__(
         self.agent_configs: list[dict] = []
         self.open_ports: list[str] = []
         self.agent_procs: dict[str, tuple[sp.Popen, str]] = {}
-        self.agent_procs_assign: dict[str, tuple[autogen.ConversableAgent, str]] = {}
+        self.agent_procs_assign: dict[str, tuple[ConversableAgent, str]] = {}
         self.cached_configs: dict = {}
 
         self.max_agents = max_agents
@@ -239,7 +240,7 @@ def _create_agent(
         member_name: list[str],
         llm_config: dict,
         use_oai_assistant: Optional[bool] = False,
-    ) -> autogen.AssistantAgent:
+    ) -> AssistantAgent:
         """"""Create a group chat participant agent.
 
         If the agent rely on an open-source model, this function will automatically set up an endpoint for that agent.
@@ -274,7 +275,7 @@ def _create_agent(
             filter_dict.update({""model"": model_name_or_hf_repo})
         if len(model_tags) > 0:
             filter_dict.update({""tags"": model_tags})
-        config_list = autogen.config_list_from_json(
+        config_list = config_list_from_json(
             self.config_file_or_env, file_location=self.config_file_location, filter_dict=filter_dict
         )
         if len(config_list) == 0:
@@ -287,7 +288,7 @@ def _create_agent(
         current_config = llm_config.copy()
         current_config.update({""config_list"": config_list})
         if use_oai_assistant:
-            from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent
+            from ..gpt_assistant_agent import GPTAssistantAgent
 
             agent = GPTAssistantAgent(
                 name=agent_name,
@@ -302,14 +303,14 @@ def _create_agent(
                     ""
The group also include a Computer_terminal to help you run the python and shell code.""
                 )
 
-            model_class = autogen.AssistantAgent
+            model_class = AssistantAgent
             if agent_path:
                 module_path, model_class_name = agent_path.replace(""/"", ""."").rsplit(""."", 1)
                 module = importlib.import_module(module_path)
                 model_class = getattr(module, model_class_name)
-                if not issubclass(model_class, autogen.ConversableAgent):
+                if not issubclass(model_class, ConversableAgent):
                     logger.error(f""{model_class} is not a ConversableAgent. Use AssistantAgent as default"")
-                    model_class = autogen.AssistantAgent
+                    model_class = AssistantAgent
 
             additional_config = {
                 k: v
@@ -365,10 +366,10 @@ def build(
         coding: Optional[bool] = None,
         code_execution_config: Optional[dict] = None,
         use_oai_assistant: Optional[bool] = False,
-        user_proxy: Optional[autogen.ConversableAgent] = None,
+        user_proxy: Optional[ConversableAgent] = None,
         max_agents: Optional[int] = None,
         **kwargs,
-    ) -> tuple[list[autogen.ConversableAgent], dict]:
+    ) -> tuple[list[ConversableAgent], dict]:
         """"""Auto build agents based on the building task.
 
         Args:
@@ -496,9 +497,9 @@ def build_from_library(
         code_execution_config: Optional[dict] = None,
         use_oai_assistant: Optional[bool] = False,
         embedding_model: Optional[str] = ""all-mpnet-base-v2"",
-        user_proxy: Optional[autogen.ConversableAgent] = None,
+        user_proxy: Optional[ConversableAgent] = None,
         **kwargs,
-    ) -> tuple[list[autogen.ConversableAgent], dict]:
+    ) -> tuple[list[ConversableAgent], dict]:
         """"""Build agents from a library.
         The library is a list of agent configs, which contains the name and system_message for each agent.
         We use a build manager to decide what agent in that library should be involved to the task.
@@ -655,8 +656,8 @@ def build_from_library(
         return self._build_agents(use_oai_assistant, user_proxy=user_proxy, **kwargs)
 
     def _build_agents(
-        self, use_oai_assistant: Optional[bool] = False, user_proxy: Optional[autogen.ConversableAgent] = None, **kwargs
-    ) -> tuple[list[autogen.ConversableAgent], dict]:
+        self, use_oai_assistant: Optional[bool] = False, user_proxy: Optional[ConversableAgent] = None, **kwargs
+    ) -> tuple[list[ConversableAgent], dict]:
         """"""Build agents with generated configs.
 
         Args:
@@ -687,7 +688,7 @@ def _build_agents(
         if coding is True:
             print(""Adding user console proxy..."", flush=True)
             if user_proxy is None:
-                user_proxy = autogen.UserProxyAgent(
+                user_proxy = UserProxyAgent(
                     name=""Computer_terminal"",
                     is_termination_msg=lambda x: x == ""TERMINATE"" or x == ""TERMINATE."",
                     code_execution_config=code_execution_config,
@@ -722,7 +723,7 @@ def load(
         config_json: Optional[str] = None,
         use_oai_assistant: Optional[bool] = False,
         **kwargs,
-    ) -> tuple[list[autogen.ConversableAgent], dict]:
+    ) -> tuple[list[ConversableAgent], dict]:
         """"""Load building configs and call the build function to complete building without calling online LLMs' api.
 
         Args: