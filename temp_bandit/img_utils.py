@@ -13,9 +13,13 @@
 from typing import Union
 
 import requests
-from PIL import Image
 
-from autogen.agentchat import utils
+from ...import_utils import optional_import_block, require_optional_import
+from .. import utils
+
+with optional_import_block():
+    from PIL import Image
+
 
 # Parameters for token counting for images for different models
 MODEL_PARAMS = {
@@ -37,7 +41,8 @@
 }
 
 
-def get_pil_image(image_file: Union[str, Image.Image]) -> Image.Image:
+@require_optional_import(""PIL"", ""unknown"")
+def get_pil_image(image_file: Union[str, ""Image.Image""]) -> ""Image.Image"":
     """"""Loads an image from a file and returns a PIL Image object.
 
     Parameters:
@@ -75,7 +80,8 @@ def get_pil_image(image_file: Union[str, Image.Image]) -> Image.Image:
     return image.convert(""RGB"")
 
 
-def get_image_data(image_file: Union[str, Image.Image], use_b64=True) -> bytes:
+@require_optional_import(""PIL"", ""unknown"")
+def get_image_data(image_file: Union[str, ""Image.Image""], use_b64=True) -> bytes:
     """"""Loads an image and returns its data either as raw bytes or in base64-encoded format.
 
     This function first loads an image from the specified file, URL, or base64 string using
@@ -105,6 +111,7 @@ def get_image_data(image_file: Union[str, Image.Image], use_b64=True) -> bytes:
         return content
 
 
+@require_optional_import(""PIL"", ""unknown"")
 def llava_formatter(prompt: str, order_image_tokens: bool = False) -> tuple[str, list[str]]:
     """"""Formats the input prompt by replacing image tags and returns the new prompt along with image locations.
 
@@ -149,7 +156,8 @@ def llava_formatter(prompt: str, order_image_tokens: bool = False) -> tuple[str,
     return new_prompt, images
 
 
-def pil_to_data_uri(image: Image.Image) -> str:
+@require_optional_import(""PIL"", ""unknown"")
+def pil_to_data_uri(image: ""Image.Image"") -> str:
     """"""Converts a PIL Image object to a data URI.
 
     Parameters:
@@ -184,6 +192,7 @@ def _get_mime_type_from_data_uri(base64_image):
     return data_uri
 
 
+@require_optional_import(""PIL"", ""unknown"")
 def gpt4v_formatter(prompt: str, img_format: str = ""uri"") -> list[Union[str, dict]]:
     """"""Formats the input prompt by replacing image tags and returns a list of text and images.
 
@@ -251,7 +260,8 @@ def extract_img_paths(paragraph: str) -> list:
     return img_paths
 
 
-def _to_pil(data: str) -> Image.Image:
+@require_optional_import(""PIL"", ""unknown"")
+def _to_pil(data: str) -> ""Image.Image"":
     """"""Converts a base64 encoded image data string to a PIL Image object.
 
     This function first decodes the base64 encoded string to bytes, then creates a BytesIO object from the bytes,
@@ -266,6 +276,7 @@ def _to_pil(data: str) -> Image.Image:
     return Image.open(BytesIO(base64.b64decode(data)))
 
 
+@require_optional_import(""PIL"", ""unknown"")
 def message_formatter_pil_to_b64(messages: list[dict]) -> list[dict]:
     """"""Converts the PIL image URLs in the messages to base64 encoded data URIs.
 
@@ -321,8 +332,9 @@ def message_formatter_pil_to_b64(messages: list[dict]) -> list[dict]:
     return new_messages
 
 
+@require_optional_import(""PIL"", ""unknown"")
 def num_tokens_from_gpt_image(
-    image_data: Union[str, Image.Image], model: str = ""gpt-4-vision"", low_quality: bool = False
+    image_data: Union[str, ""Image.Image""], model: str = ""gpt-4-vision"", low_quality: bool = False
 ) -> int:
     """"""Calculate the number of tokens required to process an image based on its dimensions
     after scaling for different GPT models. Supports ""gpt-4-vision"", ""gpt-4o"", and ""gpt-4o-mini"".