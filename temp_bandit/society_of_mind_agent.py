@@ -9,7 +9,7 @@
 import traceback
 from typing import Callable, Literal, Optional, Union
 
-from autogen import Agent, ConversableAgent, GroupChat, GroupChatManager, OpenAIWrapper
+from ... import Agent, ConversableAgent, GroupChat, GroupChatManager, OpenAIWrapper
 
 
 class SocietyOfMindAgent(ConversableAgent):