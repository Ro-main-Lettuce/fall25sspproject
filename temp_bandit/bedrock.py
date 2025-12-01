@@ -38,16 +38,20 @@
 import warnings
 from typing import Any, Literal
 
-import boto3
 import requests
-from botocore.config import Config
 from openai.types.chat import ChatCompletion, ChatCompletionMessageToolCall
 from openai.types.chat.chat_completion import ChatCompletionMessage, Choice
 from openai.types.completion_usage import CompletionUsage
 
-from autogen.oai.client_utils import validate_parameter
+from ..import_utils import optional_import_block, require_optional_import
+from .client_utils import validate_parameter
 
+with optional_import_block():
+    import boto3
+    from botocore.config import Config
 
+
+@require_optional_import(""boto3"", ""bedrock"")
 class BedrockClient:
     """"""Client for Amazon's Bedrock Converse API.""""""
 