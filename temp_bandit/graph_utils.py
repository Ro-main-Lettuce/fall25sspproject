@@ -7,7 +7,7 @@
 import logging
 from typing import Optional
 
-from autogen.agentchat import Agent
+from .agentchat import Agent
 
 
 def has_self_loops(allowed_speaker_transitions: dict) -> bool: