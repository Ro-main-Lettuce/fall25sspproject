@@ -7,14 +7,17 @@
 import re
 from typing import Any, Literal, Optional, Protocol, Union
 
-from PIL.Image import Image
 from openai import OpenAI
 
-from autogen import Agent, ConversableAgent, code_utils
-from autogen.agentchat.contrib import img_utils
-from autogen.agentchat.contrib.capabilities.agent_capability import AgentCapability
-from autogen.agentchat.contrib.text_analyzer_agent import TextAnalyzerAgent
-from autogen.cache import AbstractCache
+from .... import Agent, ConversableAgent, code_utils
+from ....cache import AbstractCache
+from ....import_utils import optional_import_block, require_optional_import
+from .. import img_utils
+from ..capabilities.agent_capability import AgentCapability
+from ..text_analyzer_agent import TextAnalyzerAgent
+
+with optional_import_block():
+    from PIL.Image import Image
 
 SYSTEM_MESSAGE = ""You've been given the special ability to generate images.""
 DESCRIPTION_MESSAGE = ""This agent has the ability to generate images.""
@@ -34,7 +37,7 @@ class ImageGenerator(Protocol):
     NOTE: Current implementation does not allow you to edit a previously existing image.
     """"""
 
-    def generate_image(self, prompt: str) -> Image:
+    def generate_image(self, prompt: str) -> ""Image"":
         """"""Generates an image based on the provided prompt.
 
         Args:
@@ -62,6 +65,7 @@ def cache_key(self, prompt: str) -> str:
         ...
 
 
+@require_optional_import(""PIL"", ""unknown"")
 class DalleImageGenerator:
     """"""Generates images using OpenAI's DALL-E models.
 
@@ -94,7 +98,7 @@ def __init__(
         self._num_images = num_images
         self._dalle_client = OpenAI(api_key=config_list[0][""api_key""])
 
-    def generate_image(self, prompt: str) -> Image:
+    def generate_image(self, prompt: str) -> ""Image"":
         response = self._dalle_client.images.generate(
             model=self._model,
             prompt=prompt,
@@ -114,6 +118,7 @@ def cache_key(self, prompt: str) -> str:
         return "","".join([str(k) for k in keys])
 
 
+@require_optional_import(""PIL"", ""unknown"")
 class ImageGeneration(AgentCapability):
     """"""This capability allows a ConversableAgent to generate images based on the message received from other Agents.
 
@@ -253,15 +258,15 @@ def _extract_prompt(self, last_message) -> str:
         analysis = self._text_analyzer.analyze_text(last_message, self._text_analyzer_instructions)
         return self._extract_analysis(analysis)
 
-    def _cache_get(self, prompt: str) -> Optional[Image]:
+    def _cache_get(self, prompt: str) -> Optional[""Image""]:
         if self._cache:
             key = self._image_generator.cache_key(prompt)
             cached_value = self._cache.get(key)
 
             if cached_value:
                 return img_utils.get_pil_image(cached_value)
 
-    def _cache_set(self, prompt: str, image: Image):
+    def _cache_set(self, prompt: str, image: ""Image""):
         if self._cache:
             key = self._image_generator.cache_key(prompt)
             self._cache.set(key, img_utils.pil_to_data_uri(image))
@@ -272,7 +277,7 @@ def _extract_analysis(self, analysis: Union[str, dict, None]) -> str:
         else:
             return code_utils.content_str(analysis)
 
-    def _generate_content_message(self, prompt: str, image: Image) -> dict[str, Any]:
+    def _generate_content_message(self, prompt: str, image: ""Image"") -> dict[str, Any]:
         return {
             ""content"": [
                 {""type"": ""text"", ""text"": f""I generated an image with the prompt: {prompt}""},