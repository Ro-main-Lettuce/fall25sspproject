@@ -29,12 +29,15 @@
 import warnings
 from typing import Any
 
-from cerebras.cloud.sdk import Cerebras, Stream
 from openai.types.chat import ChatCompletion, ChatCompletionMessageToolCall
 from openai.types.chat.chat_completion import ChatCompletionMessage, Choice
 from openai.types.completion_usage import CompletionUsage
 
-from autogen.oai.client_utils import should_hide_tools, validate_parameter
+from ..import_utils import optional_import_block, require_optional_import
+from .client_utils import should_hide_tools, validate_parameter
+
+with optional_import_block():
+    from cerebras.cloud.sdk import Cerebras, Stream
 
 CEREBRAS_PRICING_1K = {
     # Convert pricing per million to per thousand tokens.
@@ -111,6 +114,7 @@ def parse_params(self, params: dict[str, Any]) -> dict[str, Any]:
 
         return cerebras_params
 
+    @require_optional_import(""cerebras"", ""cerebras"")
     def create(self, params: dict) -> ChatCompletion:
         messages = params.get(""messages"", [])
 