@@ -29,12 +29,15 @@
 import warnings
 from typing import Any
 
-from groq import Groq, Stream
 from openai.types.chat import ChatCompletion, ChatCompletionMessageToolCall
 from openai.types.chat.chat_completion import ChatCompletionMessage, Choice
 from openai.types.completion_usage import CompletionUsage
 
-from autogen.oai.client_utils import should_hide_tools, validate_parameter
+from ..import_utils import optional_import_block, require_optional_import
+from .client_utils import should_hide_tools, validate_parameter
+
+with optional_import_block():
+    from groq import Groq, Stream
 
 # Cost per thousand tokens - Input / Output (NOTE: Convert $/Million to $/K)
 GROQ_PRICING_1K = {
@@ -126,6 +129,7 @@ def parse_params(self, params: dict[str, Any]) -> dict[str, Any]:
 
         return groq_params
 
+    @require_optional_import(""groq"", ""groq"")
     def create(self, params: dict) -> ChatCompletion:
         messages = params.get(""messages"", [])
 