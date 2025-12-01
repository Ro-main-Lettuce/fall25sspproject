@@ -7,16 +7,16 @@
 import copy
 from typing import Callable, Optional, Union
 
-from autogen.agentchat.assistant_agent import ConversableAgent
-from autogen.agentchat.contrib.capabilities.agent_capability import AgentCapability
-from autogen.agentchat.contrib.img_utils import (
+from ....code_utils import content_str
+from ....oai.client import OpenAIWrapper
+from ...assistant_agent import ConversableAgent
+from ..img_utils import (
     convert_base64_to_data_uri,
     get_image_data,
     get_pil_image,
     gpt4v_formatter,
 )
-from autogen.code_utils import content_str
-from autogen.oai.client import OpenAIWrapper
+from .agent_capability import AgentCapability
 
 DEFAULT_DESCRIPTION_PROMPT = (
     ""Write a detailed caption for this image. ""