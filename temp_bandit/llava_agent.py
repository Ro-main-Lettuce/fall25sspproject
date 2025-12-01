@@ -8,15 +8,17 @@
 import logging
 from typing import Optional
 
-import replicate
 import requests
 
-from autogen.agentchat.agent import Agent
-from autogen.agentchat.contrib.img_utils import get_image_data, llava_formatter
-from autogen.agentchat.contrib.multimodal_conversable_agent import MultimodalConversableAgent
-from autogen.code_utils import content_str
-
+from ...code_utils import content_str
 from ...formatting_utils import colored
+from ...import_utils import optional_import_block, require_optional_import
+from ..agent import Agent
+from .img_utils import get_image_data, llava_formatter
+from .multimodal_conversable_agent import MultimodalConversableAgent
+
+with optional_import_block():
+    import replicate
 
 logger = logging.getLogger(__name__)
 
@@ -95,6 +97,7 @@ def _image_reply(self, messages=None, sender=None, config=None):
         return True, out
 
 
+@require_optional_import(""replicate"", ""lmm"")
 def _llava_call_binary_with_config(
     prompt: str, images: list, config: dict, max_new_tokens: int = 1000, temperature: float = 0.5, seed: int = 1
 ):
@@ -140,6 +143,7 @@ def _llava_call_binary_with_config(
     return output
 
 
+@require_optional_import(""replicate"", ""lmm"")
 def llava_call_binary(
     prompt: str, images: list, config_list: list, max_new_tokens: int = 1000, temperature: float = 0.5, seed: int = 1
 ):