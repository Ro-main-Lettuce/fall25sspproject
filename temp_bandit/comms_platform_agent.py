@@ -12,7 +12,7 @@
 from ....messages.agent_messages import WaitingForTaskMessage
 from ...agent import Agent
 from ...conversable_agent import ConversableAgent
-from .platform_configs import BasePlatformConfig, ReplyMonitorConfig
+from .platform_configs import BaseCommsPlatformConfig, ReplyMonitorConfig
 from .platform_errors import PlatformError
 
 __NESTED_CHAT_EXECUTOR_PREFIX__ = ""Send the message (if needed)""
@@ -29,7 +29,10 @@ class PlatformMessageDecision(BaseModel):
 
 
 class PlatformDecisionAgent(ConversableAgent):
-    """"""Agent responsible for deciding what/whether to send to platform.""""""
+    """"""Agent responsible for deciding what/whether to send to platform.
+
+    This agent is part of the Nested Chat sequence and is responsible for deciding whether to send a message to the platform.
+    """"""
 
     def __init__(
         self,
@@ -45,6 +48,7 @@ def __init__(
             ""Consider message appropriateness, platform limitations, and context.""
         )
 
+        # Add the structured message to the LLM configuration
         structured_config_list = copy.deepcopy(llm_config)
         for config in structured_config_list[""config_list""]:
             config[""response_format""] = PlatformMessageDecision
@@ -60,9 +64,14 @@ def __init__(
 
 
 class PlatformExecutorAgent(ConversableAgent):
-    """"""Agent responsible for executing platform communications.""""""
+    """"""Agent responsible for executing platform communications.
+
+    This agent is part of the Nested Chat sequence and is responsible for sending messages to the platform and waiting for replies.
+    """"""
 
-    def __init__(self, platform_config: BasePlatformConfig, reply_monitor_config: Optional[ReplyMonitorConfig] = None):
+    def __init__(
+        self, platform_config: BaseCommsPlatformConfig, reply_monitor_config: Optional[ReplyMonitorConfig] = None
+    ):
         system_message = (
             ""You are a platform communication executor. ""
             ""You handle sending messages and receiving replies from the platform.""
@@ -75,7 +84,7 @@ def __init__(self, platform_config: BasePlatformConfig, reply_monitor_config: Op
 
     @abstractmethod
     def send_to_platform(self, message: str) -> Tuple[str, Optional[str]]:
-        """"""Send message to platform.
+        """"""Send a message to the platform
 
         Args:
             message: The message to send
@@ -87,7 +96,7 @@ def send_to_platform(self, message: str) -> Tuple[str, Optional[str]]:
 
     @abstractmethod
     def wait_for_reply(self, msg_id: str) -> List[dict]:
-        """"""Wait for reply from platform.
+        """"""Wait for replies to a sent message
 
         Args:
             msg_id: Message ID to monitor for replies
@@ -108,7 +117,28 @@ def cleanup_monitoring(self, msg_id: str):
 
 
 class CommsPlatformAgent(ConversableAgent):
-    """"""Base class for communication platform agents.""""""
+    """"""Base class for communication platform agents.
+
+    This class should not be used directly, but should be subclassed for specific platforms.
+
+    Examples of classes using it are DiscordAgent, SlackAgent, and TelegramAgent.
+
+    How this agent works:
+    - The agent utilizes two inner agents, a decision agent and an executor agent.
+    - The decision agent decides whether to send a message and crafts the message.
+    - The executor agent sends the message and waits for replies (optional).
+
+    The agents are used in a nested chat sequence to handle the decision and execution of the platform communication.
+
+    Args (unique or overridden in this inherited class):
+        platform_config: The configuration for the platform
+        executor_agent: The agent responsible for the platform communication (sending and monitoring for replies)
+        message_to_send: The function to determine the message to send, returns None to indicate do not send a message, otherwise determined automatically
+            Function signature:
+            def my_message_to_send(agent: ConversableAgent, messages: list[dict]) -> Union[str, None]:
+        reply_monitor_config: Configuration for monitoring replies
+        auto_reply: The message to send if no message was sent
+    """"""
 
     DEFAULT_SUMMARY_PROMPT = (
         ""Analyze the interaction about sending a message to the platform. ""
@@ -119,9 +149,8 @@ class CommsPlatformAgent(ConversableAgent):
     def __init__(
         self,
         name: str,
-        platform_config: ""BasePlatformConfig"",
+        platform_config: ""BaseCommsPlatformConfig"",
         executor_agent: ""PlatformExecutorAgent"",
-        send_config: Dict[str, Any],
         message_to_send: Optional[
             callable
         ] = None,  # The function to determine the message to send, returns None to indicate do not send a message, otherwise determined automatically
@@ -134,14 +163,15 @@ def __init__(
     ):
         super().__init__(name=name, system_message=system_message, llm_config=llm_config, *args, **kwargs)
 
-        # self.message_to_send = message_to_send
         # Are we using an LLM to decide and create the message?
         self.message_decision_creation_llm = message_to_send is None
+
+        # The function to determine the message to send (optional)
         self.message_to_send = message_to_send
 
-        # Create our specialized agents
-        self.executor_agent = executor_agent
+        # Our two inner agents
         self.decision_agent = PlatformDecisionAgent(self.__class__.__name__.replace(""Agent"", """"), llm_config=llm_config)
+        self.executor_agent = executor_agent
 
         if message_to_send:
             # If we are using the callable to determine the message to send, update the decision_agent to use their function instead of the LLM
@@ -153,7 +183,7 @@ def __init__(
 
         # Register the reply function on the executor agent that will trigger in the second chat in the nested chat sequence
         self.executor_agent.register_reply(
-            trigger=[ConversableAgent],  # , None],
+            trigger=[ConversableAgent],
             reply_func=self._executor_reply_function,
             remove_other_reply_funcs=True,
         )
@@ -181,7 +211,7 @@ def __init__(
             ],
             trigger=[ConversableAgent],
             position=0,
-            use_async=False,
+            use_async=False,  # This will run the nested chat sequence synchronously, even if the outer chat is async
         )
 
         # Reply configuration
@@ -194,7 +224,15 @@ def _process_message_to_send(
         sender: Optional[Agent] = None,
         config: Optional[Any] = None,
     ) -> Tuple[bool, Union[str, Dict, None]]:
-        """"""Execute the message_to_send and returns our structured output for compatibility with the executor agent's processing.""""""
+        """"""Execute the message_to_send and returns our structured output for compatibility with the executor agent's processing.
+
+        This is a reply function associated with the decision agent.
+
+        Args as per reply function signature.
+
+        Returns:
+            Tuple[bool, Union[str, Dict, None]]: A tuple of (completed, response_message)
+        """"""
 
         # Get the message to send
         message = self.message_to_send(self, messages)
@@ -207,7 +245,14 @@ def _process_message_to_send(
     def _executor_message_validation(
         self, message_content: str
     ) -> Tuple[bool, Optional[PlatformMessageDecision], Optional[str]]:
-        """"""Shared validation logic for both sync and async versions.""""""
+        """"""Validates the structured output received by the decision agent
+
+        Args:
+            message_content: The message content to validate, should be a structured output JSON with the nested chat prefix content
+
+        Returns:
+            Tuple[bool, Optional[PlatformMessageDecision], Optional[str]]: A tuple of (is_valid, decision structured output, error_message)
+        """"""
         # Check message prefix
         if not message_content.startswith(f""{__NESTED_CHAT_EXECUTOR_PREFIX__}
Context: 
""):
             return False, None, ""Error, the workflow did not work correctly, message not sent.""
@@ -235,7 +280,13 @@ def _executor_reply_function(
         """"""Enhanced executor reply function that handles sending and waiting for replies.
 
         Handles all platform-specific errors and provides detailed status reporting.
-        Returns a tuple of (completed, response_message).
+
+        This is a reply function associated with the executor agent.
+
+        Args as per reply function signature.
+
+        Returns:
+            Tuple[bool, Union[str, Dict, None]]: A tuple of (completed, response_message)
         """"""
         message_content: str = messages[-1][""content""]
 
@@ -300,7 +351,17 @@ def _executor_reply_function(
         return True, ""No message was sent based on decision""
 
     def _prepare_decision_message(self, recipient: Agent, messages: List[Dict[str, Any]], sender: Agent, config) -> str:
-        """"""Prepare message for decision agent based on conversation history.""""""
+        """"""Prepare message for decision agent based on conversation history for the first chat in the nested chat
+
+        Args: (as per Callable signature in ConversableAgent._get_chats_to_run)
+            recipient (Agent): The recipient agent
+            messages (Union[str, Callable]): The messages in the conversation history
+            sender (Agent): The sender agent
+            config (Any): Any configuration
+
+        Returns:
+            str: The message for the decision agent to act on.
+        """"""
 
         # Compile the list of messages into a single string with the name value and the content value. Ignore anything where the role contains tool'
         # name and/or role may not be present