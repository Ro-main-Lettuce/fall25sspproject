@@ -30,15 +30,18 @@
 import warnings
 from typing import Any, Optional, Type
 
-import ollama
-from fix_busted_json import repair_json
-from ollama import Client
 from openai.types.chat import ChatCompletion, ChatCompletionMessageToolCall
 from openai.types.chat.chat_completion import ChatCompletionMessage, Choice
 from openai.types.completion_usage import CompletionUsage
 from pydantic import BaseModel
 
-from autogen.oai.client_utils import FormatterProtocol, should_hide_tools, validate_parameter
+from ..import_utils import optional_import_block, require_optional_import
+from .client_utils import FormatterProtocol, should_hide_tools, validate_parameter
+
+with optional_import_block():
+    import ollama
+    from fix_busted_json import repair_json
+    from ollama import Client
 
 
 class OllamaClient:
@@ -176,6 +179,7 @@ def parse_params(self, params: dict[str, Any]) -> dict[str, Any]:
 
         return ollama_params
 
+    @require_optional_import([""ollama"", ""fix_busted_json""], ""ollama"")
     def create(self, params: dict) -> ChatCompletion:
         messages = params.get(""messages"", [])
 
@@ -497,6 +501,7 @@ def _format_json_response(response: Any, original_answer: str) -> str:
     return response.format() if isinstance(response, FormatterProtocol) else original_answer
 
 
+@require_optional_import(""fix_busted_json"", ""ollama"")
 def response_to_tool_call(response_string: str) -> Any:
     """"""Attempts to convert the response to an object, aimed to align with function format `[{},{}]`""""""
     # We try and detect the list[dict] format: