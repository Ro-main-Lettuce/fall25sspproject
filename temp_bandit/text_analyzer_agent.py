@@ -6,8 +6,8 @@
 # SPDX-License-Identifier: MIT
 from typing import Any, Literal, Optional, Union
 
-from autogen.agentchat.agent import Agent
-from autogen.agentchat.assistant_agent import ConversableAgent
+from ..agent import Agent
+from ..assistant_agent import ConversableAgent
 
 system_message = """"""You are an expert in text analysis.
 The user will give you TEXT to analyze.