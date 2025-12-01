@@ -52,40 +52,44 @@
 from io import BytesIO
 from typing import Any, Optional, Type
 
-import google.generativeai as genai
 import requests
-import vertexai
-from PIL import Image
-from google.ai.generativelanguage import Content, FunctionCall, FunctionDeclaration, FunctionResponse, Part, Tool
-from google.ai.generativelanguage_v1beta.types import Schema
-from google.auth.credentials import Credentials
-from google.generativeai.types import GenerateContentResponse
-from jsonschema import ValidationError
 from openai.types.chat import ChatCompletion, ChatCompletionMessageToolCall
 from openai.types.chat.chat_completion import ChatCompletionMessage, Choice
 from openai.types.completion_usage import CompletionUsage
 from pydantic import BaseModel
-from vertexai.generative_models import (
-    Content as VertexAIContent,
-)
-from vertexai.generative_models import FunctionDeclaration as vaiFunctionDeclaration
-from vertexai.generative_models import (
-    GenerationResponse as VertexAIGenerationResponse,
-)
-from vertexai.generative_models import GenerativeModel
-from vertexai.generative_models import HarmBlockThreshold as VertexAIHarmBlockThreshold
-from vertexai.generative_models import HarmCategory as VertexAIHarmCategory
-from vertexai.generative_models import Part as VertexAIPart
-from vertexai.generative_models import SafetySetting as VertexAISafetySetting
-from vertexai.generative_models import (
-    Tool as vaiTool,
-)
-
-from autogen.oai.client_utils import FormatterProtocol
+
+from ..import_utils import optional_import_block, require_optional_import
+from .client_utils import FormatterProtocol
+
+with optional_import_block():
+    import google.generativeai as genai
+    import vertexai
+    from PIL import Image
+    from google.ai.generativelanguage import Content, FunctionCall, FunctionDeclaration, FunctionResponse, Part, Tool
+    from google.ai.generativelanguage_v1beta.types import Schema
+    from google.auth.credentials import Credentials
+    from google.generativeai.types import GenerateContentResponse
+    from jsonschema import ValidationError
+    from vertexai.generative_models import (
+        Content as VertexAIContent,
+    )
+    from vertexai.generative_models import FunctionDeclaration as vaiFunctionDeclaration
+    from vertexai.generative_models import (
+        GenerationResponse as VertexAIGenerationResponse,
+    )
+    from vertexai.generative_models import GenerativeModel
+    from vertexai.generative_models import HarmBlockThreshold as VertexAIHarmBlockThreshold
+    from vertexai.generative_models import HarmCategory as VertexAIHarmCategory
+    from vertexai.generative_models import Part as VertexAIPart
+    from vertexai.generative_models import SafetySetting as VertexAISafetySetting
+    from vertexai.generative_models import (
+        Tool as vaiTool,
+    )
 
 logger = logging.getLogger(__name__)
 
 
+@require_optional_import([""google"", ""vertexai"", ""PIL"", ""jsonschema""], ""gemini"")
 class GeminiClient:
     """"""Client for Google's Gemini API.""""""
 
@@ -446,7 +450,7 @@ def _oai_content_to_gemini_content(self, message: dict[str, Any]) -> tuple[list,
         else:
             raise Exception(""Unable to convert content to Gemini format."")
 
-    def _concat_parts(self, parts: list[Part]) -> list:
+    def _concat_parts(self, parts: list[""Part""]) -> list:
         """"""Concatenate parts with the same type.
         If two adjacent parts both have the ""text"" attribute, then it will be joined into one part.
         """"""
@@ -563,7 +567,7 @@ def _convert_json_response(self, response: str) -> Any:
                 f""Failed to parse response as valid JSON matching the schema for Structured Output: {str(e)}""
             )
 
-    def _tools_to_gemini_tools(self, tools: list[dict[str, Any]]) -> list[Tool]:
+    def _tools_to_gemini_tools(self, tools: list[dict[str, Any]]) -> list[""Tool""]:
         """"""Create Gemini tools (as typically requires Callables)""""""
         functions = []
         for tool in tools:
@@ -583,7 +587,7 @@ def _tools_to_gemini_tools(self, tools: list[dict[str, Any]]) -> list[Tool]:
             return [Tool(function_declarations=functions)]
 
     @staticmethod
-    def _create_gemini_function_declaration(tool: dict) -> FunctionDeclaration:
+    def _create_gemini_function_declaration(tool: dict) -> ""FunctionDeclaration"":
         function_declaration = FunctionDeclaration()
         function_declaration.name = tool[""function""][""name""]
         function_declaration.description = tool[""function""][""description""]
@@ -595,7 +599,7 @@ def _create_gemini_function_declaration(tool: dict) -> FunctionDeclaration:
         return function_declaration
 
     @staticmethod
-    def _create_gemini_function_declaration_schema(json_data) -> Schema:
+    def _create_gemini_function_declaration_schema(json_data) -> ""Schema"":
         """"""Recursively creates Schema objects for FunctionDeclaration.""""""
         param_schema = Schema()
         param_type = json_data[""type""]
@@ -705,6 +709,7 @@ def _to_json_or_str(data: str) -> dict | str:
             return data
 
 
+@require_optional_import([""PIL""], ""gemini"")
 def get_image_data(image_file: str, use_b64=True) -> bytes:
     if image_file.startswith(""http://"") or image_file.startswith(""https://""):
         response = requests.get(image_file)