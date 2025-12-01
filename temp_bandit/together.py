@@ -38,9 +38,12 @@
 from openai.types.chat import ChatCompletion, ChatCompletionMessageToolCall
 from openai.types.chat.chat_completion import ChatCompletionMessage, Choice
 from openai.types.completion_usage import CompletionUsage
-from together import Together
 
-from autogen.oai.client_utils import should_hide_tools, validate_parameter
+from ..import_utils import optional_import_block, require_optional_import
+from .client_utils import should_hide_tools, validate_parameter
+
+with optional_import_block():
+    from together import Together
 
 
 class TogetherClient:
@@ -129,6 +132,7 @@ def parse_params(self, params: dict[str, Any]) -> dict[str, Any]:
 
         return together_params
 
+    @require_optional_import(""together"", ""together"")
     def create(self, params: dict) -> ChatCompletion:
         messages = params.get(""messages"", [])
 