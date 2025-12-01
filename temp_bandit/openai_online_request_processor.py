@@ -1,7 +1,6 @@
 import datetime
 import logging
 import os
-import re
 import time
 from typing import TypeVar
 
@@ -10,16 +9,18 @@
 import requests
 import tiktoken
 
-from bespokelabs.curator.request_processor import APIRequest, BaseOnlineRequestProcessor
 from bespokelabs.curator.request_processor.config import OnlineRequestProcessorConfig
+from bespokelabs.curator.request_processor.online.base_online_request_processor import APIRequest, BaseOnlineRequestProcessor
 from bespokelabs.curator.request_processor.openai_request_mixin import OpenAIRequestMixin
-from bespokelabs.curator.status_tracker import OnlineStatusTracker
+from bespokelabs.curator.status_tracker.online_status_tracker import OnlineStatusTracker
 from bespokelabs.curator.types.generic_request import GenericRequest
 from bespokelabs.curator.types.generic_response import GenericResponse, TokenUsage
 
 T = TypeVar(""T"")
 logger = logger = logging.getLogger(__name__)
 
+_DEFAULT_OPENAI_URL: str = ""https://api.openai.com/v1/chat/completions""
+
 
 class OpenAIOnlineRequestProcessor(BaseOnlineRequestProcessor, OpenAIRequestMixin):
     """"""OpenAI-specific implementation of the OnlineRequestProcessor.
@@ -34,17 +35,29 @@ class OpenAIOnlineRequestProcessor(BaseOnlineRequestProcessor, OpenAIRequestMixi
         - Supports structured output via JSON schema
     """"""
 
+    _DEFAULT_COMPLETION_SUFFIX = ""/chat/completions""
+
     def __init__(self, config: OnlineRequestProcessorConfig):
+        """"""Initialize the OpenAIOnlineRequestProcessor.""""""
         super().__init__(config)
+
         if self.config.base_url is None:
-            self.url = ""https://api.openai.com/v1/chat/completions""
+            if ""OPENAI_BASE_URL"" in os.environ:
+                key_url = os.environ[""OPENAI_BASE_URL""].strip().rstrip(""/"")
+                self.url = key_url + self._DEFAULT_COMPLETION_SUFFIX
+            else:
+                self.url = _DEFAULT_OPENAI_URL
         else:
-            self.url = self.config.base_url + ""/chat/completions""
+            self.url = self.config.base_url + self._DEFAULT_COMPLETION_SUFFIX
+
         self.api_key = os.getenv(""OPENAI_API_KEY"")
         self.token_encoding = self.get_token_encoding()
-        self.header_based_max_requests_per_minute, self.header_based_max_tokens_per_minute = (
-            self.get_header_based_rate_limits()
-        )
+        self.header_based_max_requests_per_minute, self.header_based_max_tokens_per_minute = self.get_header_based_rate_limits()
+
+    @property
+    def backend(self):
+        """"""Backend property.""""""
+        return ""openai""
 
     def get_header_based_rate_limits(self) -> tuple[int, int]:
         """"""Get rate limits from OpenAI API headers.
@@ -56,9 +69,7 @@ def get_header_based_rate_limits(self) -> tuple[int, int]:
             - Makes a dummy request to get actual rate limits
         """"""
         if not self.api_key:
-            raise ValueError(
-                ""Missing OpenAI API Key - Please set OPENAI_API_KEY in your environment vars""
-            )
+            raise ValueError(""Missing OpenAI API Key - Please set OPENAI_API_KEY in your environment vars"")
 
         response = requests.post(
             self.url,
@@ -108,9 +119,7 @@ def estimate_total_tokens(self, messages: list) -> int:
                 try:
                     num_tokens += len(self.token_encoding.encode(str(value), disallowed_special=()))
                 except TypeError:
-                    logger.warning(
-                        f""Failed to encode value {value} with tiktoken. Assuming 1 token per 4 chars.""
-                    )
+                    logger.warning(f""Failed to encode value {value} with tiktoken. Assuming 1 token per 4 chars."")
                     num_tokens += len(str(value)) // 4
                 if key == ""name"":  # if there's a name, the role is omitted
                     num_tokens -= 1  # role is always required and always 1 token
@@ -149,9 +158,7 @@ def check_structured_output_support(self) -> bool:
                 return True
         if ""o1-"" in model_name:
             base_date = datetime.datetime.strptime(model_name.split(""o1-"")[1], ""%Y-%m-%d"")
-            if base_date >= datetime.datetime(
-                2024, 12, 17
-            ):  # Support o1 dated versions from 2024-12-17
+            if base_date >= datetime.datetime(2024, 12, 17):  # Support o1 dated versions from 2024-12-17
                 return True
 
         return False