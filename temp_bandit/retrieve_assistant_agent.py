@@ -7,8 +7,8 @@
 import warnings
 from typing import Any, Optional, Union
 
-from autogen.agentchat.agent import Agent
-from autogen.agentchat.assistant_agent import AssistantAgent
+from ..agent import Agent
+from ..assistant_agent import AssistantAgent
 
 
 class RetrieveAssistantAgent(AssistantAgent):