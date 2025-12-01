@@ -37,13 +37,17 @@
 import warnings
 from typing import Any
 
-from cohere import Client as Cohere
-from cohere.types import ToolParameterDefinitionsValue, ToolResult
 from openai.types.chat import ChatCompletion, ChatCompletionMessageToolCall
 from openai.types.chat.chat_completion import ChatCompletionMessage, Choice
 from openai.types.completion_usage import CompletionUsage
 
-from autogen.oai.client_utils import logging_formatter, validate_parameter
+from ..import_utils import optional_import_block, require_optional_import
+from .client_utils import logging_formatter, validate_parameter
+
+with optional_import_block():
+    from cohere import Client as Cohere
+    from cohere.types import ToolParameterDefinitionsValue, ToolResult
+
 
 logger = logging.getLogger(__name__)
 if not logger.handlers:
@@ -151,6 +155,7 @@ def parse_params(self, params: dict[str, Any]) -> dict[str, Any]:
 
         return cohere_params
 
+    @require_optional_import(""cohere"", ""cohere"")
     def create(self, params: dict) -> ChatCompletion:
         messages = params.get(""messages"", [])
         client_name = params.get(""client_name"") or ""autogen-cohere""
@@ -262,6 +267,7 @@ def create(self, params: dict) -> ChatCompletion:
         return response_oai
 
 
+@require_optional_import(""cohere"", ""cohere"")
 def extract_to_cohere_tool_results(tool_call_id: str, content_output: str, all_tool_calls) -> list[dict[str, Any]]:
     temp_tool_results = []
 
@@ -278,6 +284,7 @@ def extract_to_cohere_tool_results(tool_call_id: str, content_output: str, all_t
     return temp_tool_results
 
 
+@require_optional_import(""cohere"", ""cohere"")
 def oai_messages_to_cohere_messages(
     messages: list[dict[str, Any]], params: dict[str, Any], cohere_params: dict[str, Any]
 ) -> tuple[list[dict[str, Any]], str, str]: