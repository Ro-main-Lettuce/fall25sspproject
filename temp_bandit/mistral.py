@@ -31,25 +31,29 @@
 import warnings
 from typing import Any, Union
 
-# Mistral libraries
-# pip install mistralai
-from mistralai import (
-    AssistantMessage,
-    Function,
-    FunctionCall,
-    Mistral,
-    SystemMessage,
-    ToolCall,
-    ToolMessage,
-    UserMessage,
-)
 from openai.types.chat import ChatCompletion, ChatCompletionMessageToolCall
 from openai.types.chat.chat_completion import ChatCompletionMessage, Choice
 from openai.types.completion_usage import CompletionUsage
 
-from autogen.oai.client_utils import should_hide_tools, validate_parameter
-
-
+from ..import_utils import optional_import_block, require_optional_import
+from .client_utils import should_hide_tools, validate_parameter
+
+with optional_import_block():
+    # Mistral libraries
+    # pip install mistralai
+    from mistralai import (
+        AssistantMessage,
+        Function,
+        FunctionCall,
+        Mistral,
+        SystemMessage,
+        ToolCall,
+        ToolMessage,
+        UserMessage,
+    )
+
+
+@require_optional_import(""mistralai"", ""mistral"")
 class MistralAIClient:
     """"""Client for Mistral.AI's API.""""""
 
@@ -80,6 +84,7 @@ def message_retrieval(self, response: ChatCompletion) -> Union[list[str], list[C
     def cost(self, response) -> float:
         return response.cost
 
+    @require_optional_import(""mistralai"", ""mistral"")
     def parse_params(self, params: dict[str, Any]) -> dict[str, Any]:
         """"""Loads the parameters for Mistral.AI API from the passed in parameters and returns a validated set. Checks types, ranges, and sets defaults""""""
         mistral_params = {}
@@ -169,6 +174,7 @@ def parse_params(self, params: dict[str, Any]) -> dict[str, Any]:
 
         return mistral_params
 
+    @require_optional_import(""mistralai"", ""mistral"")
     def create(self, params: dict[str, Any]) -> ChatCompletion:
         # 1. Parse parameters to Mistral.AI API's parameters
         mistral_params = self.parse_params(params)
@@ -232,6 +238,7 @@ def get_usage(response: ChatCompletion) -> dict:
         }
 
 
+@require_optional_import(""mistralai"", ""mistral"")
 def tool_def_to_mistral(tool_definitions: list[dict[str, Any]]) -> list[dict[str, Any]]:
     """"""Converts AutoGen tool definition to a mistral tool format""""""
     mistral_tools = []