@@ -104,67 +104,66 @@ def __init__(
         silent: Optional[bool] = None,
         context_variables: Optional[dict[str, Any]] = None,
     ):
-        """"""Args:
-        name (str): name of the agent.
-        system_message (str or list): system message for the ChatCompletion inference.
-        is_termination_msg (function): a function that takes a message in the form of a dictionary
-            and returns a boolean value indicating if this received message is a termination message.
-            The dict can contain the following keys: ""content"", ""role"", ""name"", ""function_call"".
-        max_consecutive_auto_reply (int): the maximum number of consecutive auto replies.
-            default to None (no limit provided, class attribute MAX_CONSECUTIVE_AUTO_REPLY will be used as the limit in this case).
-            When set to 0, no auto reply will be generated.
-        human_input_mode (str): whether to ask for human inputs every time a message is received.
-            Possible values are ""ALWAYS"", ""TERMINATE"", ""NEVER"".
-            (1) When ""ALWAYS"", the agent prompts for human input every time a message is received.
-                Under this mode, the conversation stops when the human input is ""exit"",
-                or when is_termination_msg is True and there is no human input.
-            (2) When ""TERMINATE"", the agent only prompts for human input only when a termination message is received or
-                the number of auto reply reaches the max_consecutive_auto_reply.
-            (3) When ""NEVER"", the agent will never prompt for human input. Under this mode, the conversation stops
-                when the number of auto reply reaches the max_consecutive_auto_reply or when is_termination_msg is True.
-        function_map (dict[str, callable]): Mapping function names (passed to openai) to callable functions, also used for tool calls.
-        code_execution_config (dict or False): config for the code execution.
-            To disable code execution, set to False. Otherwise, set to a dictionary with the following keys:
-            - work_dir (Optional, str): The working directory for the code execution.
-                If None, a default working directory will be used.
-                The default working directory is the ""extensions"" directory under
-                ""path_to_autogen"".
-            - use_docker (Optional, list, str or bool): The docker image to use for code execution.
-                Default is True, which means the code will be executed in a docker container. A default list of images will be used.
-                If a list or a str of image name(s) is provided, the code will be executed in a docker container
-                with the first image successfully pulled.
-                If False, the code will be executed in the current environment.
-                We strongly recommend using docker for code execution.
-            - timeout (Optional, int): The maximum execution time in seconds.
-            - last_n_messages (Experimental, int or str): The number of messages to look back for code execution.
-                If set to 'auto', it will scan backwards through all messages arriving since the agent last spoke, which is typically the last time execution was attempted. (Default: auto)
-        llm_config (dict or False or None): llm inference configuration.
-            Please refer to [OpenAIWrapper.create](/docs/reference/oai/client#create)
-            for available options.
-            When using OpenAI or Azure OpenAI endpoints, please specify a non-empty 'model' either in `llm_config` or in each config of 'config_list' in `llm_config`.
-            To disable llm-based auto reply, set to False.
-            When set to None, will use self.DEFAULT_CONFIG, which defaults to False.
-        default_auto_reply (str or dict): default auto reply when no code execution or llm-based reply is generated.
-        description (str): a short description of the agent. This description is used by other agents
-            (e.g. the GroupChatManager) to decide when to call upon this agent. (Default: system_message)
-        chat_messages (dict or None): the previous chat messages that this agent had in the past with other agents.
-            Can be used to give the agent a memory by providing the chat history. This will allow the agent to
-            resume previous had conversations. Defaults to an empty chat history.
-        silent (bool or None): (Experimental) whether to print the message sent. If None, will use the value of
-            silent in each function.
-        context_variables (dict or None): Context variables that provide a persistent context for the agent.
-            Note: Will maintain a reference to the passed in context variables (enabling a shared context)
-            Only used in Swarms at this stage:
-            https://docs.ag2.ai/docs/reference/agentchat/contrib/swarm_agent
+        """"""
+        Args:
+            name (str): name of the agent.
+            system_message (str or list): system message for the ChatCompletion inference.
+            is_termination_msg (function): a function that takes a message in the form of a dictionary
+                and returns a boolean value indicating if this received message is a termination message.
+                The dict can contain the following keys: ""content"", ""role"", ""name"", ""function_call"".
+            max_consecutive_auto_reply (int): the maximum number of consecutive auto replies.
+                default to None (no limit provided, class attribute MAX_CONSECUTIVE_AUTO_REPLY will be used as the limit in this case).
+                When set to 0, no auto reply will be generated.
+            human_input_mode (str): whether to ask for human inputs every time a message is received.
+                Possible values are ""ALWAYS"", ""TERMINATE"", ""NEVER"".
+                (1) When ""ALWAYS"", the agent prompts for human input every time a message is received.
+                    Under this mode, the conversation stops when the human input is ""exit"",
+                    or when is_termination_msg is True and there is no human input.
+                (2) When ""TERMINATE"", the agent only prompts for human input only when a termination message is received or
+                    the number of auto reply reaches the max_consecutive_auto_reply.
+                (3) When ""NEVER"", the agent will never prompt for human input. Under this mode, the conversation stops
+                    when the number of auto reply reaches the max_consecutive_auto_reply or when is_termination_msg is True.
+            function_map (dict[str, callable]): Mapping function names (passed to openai) to callable functions, also used for tool calls.
+            code_execution_config (dict or False): config for the code execution.
+                To disable code execution, set to False. Otherwise, set to a dictionary with the following keys:
+                - work_dir (Optional, str): The working directory for the code execution.
+                    If None, a default working directory will be used.
+                    The default working directory is the ""extensions"" directory under
+                    ""path_to_autogen"".
+                - use_docker (Optional, list, str or bool): The docker image to use for code execution.
+                    Default is True, which means the code will be executed in a docker container. A default list of images will be used.
+                    If a list or a str of image name(s) is provided, the code will be executed in a docker container
+                    with the first image successfully pulled.
+                    If False, the code will be executed in the current environment.
+                    We strongly recommend using docker for code execution.
+                - timeout (Optional, int): The maximum execution time in seconds.
+                - last_n_messages (Experimental, int or str): The number of messages to look back for code execution.
+                    If set to 'auto', it will scan backwards through all messages arriving since the agent last spoke, which is typically the last time execution was attempted. (Default: auto)
+            llm_config (dict or False or None): llm inference configuration.
+                Please refer to [OpenAIWrapper.create](/docs/reference/oai/client#create)
+                for available options.
+                When using OpenAI or Azure OpenAI endpoints, please specify a non-empty 'model' either in `llm_config` or in each config of 'config_list' in `llm_config`.
+                To disable llm-based auto reply, set to False.
+                When set to None, will use self.DEFAULT_CONFIG, which defaults to False.
+            default_auto_reply (str or dict): default auto reply when no code execution or llm-based reply is generated.
+            description (str): a short description of the agent. This description is used by other agents
+                (e.g. the GroupChatManager) to decide when to call upon this agent. (Default: system_message)
+            chat_messages (dict or None): the previous chat messages that this agent had in the past with other agents.
+                Can be used to give the agent a memory by providing the chat history. This will allow the agent to
+                resume previous had conversations. Defaults to an empty chat history.
+            silent (bool or None): (Experimental) whether to print the message sent. If None, will use the value of
+                silent in each function.
+            context_variables (dict or None): Context variables that provide a persistent context for the agent.
+                Note: Will maintain a reference to the passed in context variables (enabling a shared context)
+                Only used in Swarms at this stage:
+                https://docs.ag2.ai/docs/reference/agentchat/contrib/swarm_agent
         """"""
         # we change code_execution_config below and we have to make sure we don't change the input
         # in case of UserProxyAgent, without this we could even change the default value {}
         code_execution_config = (
             code_execution_config.copy() if hasattr(code_execution_config, ""copy"") else code_execution_config
         )
 
-        self._validate_name(name)
-        self._name = name
         # a dictionary of conversations, default value is list
         if chat_messages is None:
             self._oai_messages = defaultdict(list)
@@ -190,6 +189,8 @@ def __init__(
                 ) from e
 
         self._validate_llm_config(llm_config)
+        self._validate_name(name)
+        self._name = name
 
         if logging_enabled():
             log_new_agent(self, locals())
@@ -285,6 +286,15 @@ def __init__(
         }
 
     def _validate_name(self, name: str) -> None:
+        if not self.llm_config or ""config_list"" not in self.llm_config or len(self.llm_config[""config_list""]) == 0:
+            return
+
+        config_list = self.llm_config.get(""config_list"")
+        # The validation is currently done only for openai endpoints
+        # (other ones do not have the issue with whitespace in the name)
+        if ""api_type"" in config_list[0] and config_list[0][""api_type""] != ""openai"":
+            return
+
         # Validation for name using regex to detect any whitespace
         if re.search(r""\s"", name):
             raise ValueError(f""The name of the agent cannot contain any whitespace. The name provided is: '{name}'"")
@@ -1894,12 +1904,12 @@ async def a_check_termination_and_human_reply(
         for the conversation and prints relevant messages based on the human input received.
 
         Args:
-            - messages (Optional[List[Dict]]): A list of message dictionaries, representing the conversation history.
-            - sender (Optional[Agent]): The agent object representing the sender of the message.
-            - config (Optional[Any]): Configuration object, defaults to the current instance if not provided.
+            messages (Optional[List[Dict]]): A list of message dictionaries, representing the conversation history.
+            sender (Optional[Agent]): The agent object representing the sender of the message.
+            config (Optional[Any]): Configuration object, defaults to the current instance if not provided.
 
         Returns:
-            - Tuple[bool, Union[str, Dict, None]]: A tuple containing a boolean indicating if the conversation
+            Tuple[bool, Union[str, Dict, None]]: A tuple containing a boolean indicating if the conversation
             should be terminated, and a human reply which can be a string, a dictionary, or None.
         """"""
         iostream = IOStream.get_default()