@@ -7,15 +7,14 @@
 import copy
 from typing import Optional, Union
 
-from autogen import OpenAIWrapper
-from autogen.agentchat import Agent, ConversableAgent
-from autogen.agentchat.contrib.img_utils import (
+from ... import OpenAIWrapper
+from ..._pydantic import model_dump
+from ...code_utils import content_str
+from .. import Agent, ConversableAgent
+from ..contrib.img_utils import (
     gpt4v_formatter,
     message_formatter_pil_to_b64,
 )
-from autogen.code_utils import content_str
-
-from ..._pydantic import model_dump
 
 DEFAULT_LMM_SYS_MSG = """"""You are a helpful AI assistant.""""""
 DEFAULT_MODEL = ""gpt-4-vision-preview""