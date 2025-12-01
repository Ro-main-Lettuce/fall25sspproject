@@ -1,27 +1,26 @@
-import logging
-from typing import Optional
-import vllm
-import datetime
-from bespokelabs.curator.request_processor.online.base_online_request_processor import APIRequest
-from bespokelabs.curator.request_processor import BaseOfflineRequestProcessor
-from bespokelabs.curator.status_tracker import OfflineStatusTracker
-from bespokelabs.curator.types.generic_request import GenericRequest
-from bespokelabs.curator.types.generic_response import TokenUsage, GenericResponse
-from vllm.distributed import destroy_model_parallel, destroy_distributed_environment
 import contextlib
-import torch
+import datetime
 import gc
+import logging
+
+import torch
+import vllm
+from pydantic import BaseModel
+from vllm.distributed import destroy_distributed_environment, destroy_model_parallel
 from vllm.sampling_params import GuidedDecodingParams
+
 from bespokelabs.curator.request_processor.config import OfflineRequestProcessorConfig
-from pydantic import BaseModel
-from typing import List
+from bespokelabs.curator.request_processor.offline.base_offline_request_processor import BaseOfflineRequestProcessor
+from bespokelabs.curator.request_processor.online.base_online_request_processor import APIRequest
+from bespokelabs.curator.status_tracker.offline_status_tracker import OfflineStatusTracker
+from bespokelabs.curator.types.generic_request import GenericRequest
+from bespokelabs.curator.types.generic_response import GenericResponse
 
 logger = logging.getLogger(__name__)
 
 
 class VLLMOfflineRequestProcessor(BaseOfflineRequestProcessor):
-    """"""
-    Offline request processor for the VLLM model.
+    """"""Offline request processor for the VLLM model.
 
     Args:
         config (OfflineRequestProcessorConfig): Configuration for the request processor
@@ -31,10 +30,16 @@ def __init__(
         self,
         config: OfflineRequestProcessorConfig,
     ):
+        """"""Initialize the VLLMOfflineRequestProcessor.""""""
         super().__init__(
             config,
         )
 
+    @property
+    def backend(self):
+        """"""Backend property.""""""
+        return ""vllm""
+
     def load_offline_model(self):
         """"""Load the VLLM model for offline processing.""""""
         self.model_class = vllm.LLM(
@@ -54,15 +59,9 @@ def format_prompts(self, prompts: list) -> list:
         Args:
             prompts (list): List of prompts to format
         """"""
-
         tokenizer = self.model_class.get_tokenizer()
         try:
-            formatted_prompts = [
-                tokenizer.apply_chat_template(
-                    conversation=prompt, tokenize=False, add_generation_prompt=True
-                )
-                for prompt in prompts
-            ]
+            formatted_prompts = [tokenizer.apply_chat_template(conversation=prompt, tokenize=False, add_generation_prompt=True) for prompt in prompts]
         except Exception as e:
             logger.error(f""Error formatting prompts: {e}"")
             raise e
@@ -83,7 +82,6 @@ def check_structured_output_support(self) -> bool:
             - Logs detailed information about support status
             - Required for models that will use JSON schema responses
         """"""
-
         self.load_offline_model()
 
         class User(BaseModel):
@@ -108,16 +106,11 @@ class User(BaseModel):
             assert isinstance(response.name, str)
             assert response.name == ""Jason""
             assert response.age == 25
-            logger.info(
-                f""Model {self.model} supports structured output via instructor, response: {response}""
-            )
+            logger.info(f""Model {self.model} supports structured output via instructor, response: {response}"")
             self.support_structured_output = True
             return True
         except Exception as e:
-
-            logger.warning(
-                f""Model {self.model} does not support structured output via guided decoding: {e} {type(e)} {e}""
-            )
+            logger.warning(f""Model {self.model} does not support structured output via guided decoding: {e} {type(e)} {e}"")
             return False
 
     def create_api_specific_request(self, generic_request: GenericRequest) -> dict:
@@ -135,7 +128,6 @@ def create_api_specific_request(self, generic_request: GenericRequest) -> dict:
         Note:
             Uses vLLM's get_supported_openai_params to check parameter support
         """"""
-
         request = {
             ""model"": generic_request.model,
             ""messages"": generic_request.messages,
@@ -157,27 +149,27 @@ def destroy(self):
         torch.cuda.synchronize()
 
     def fix_json(self, response_message: str) -> str:
-        """"""
-        Fix vLLM issue (https://github.com/vllm-project/vllm/issues/8350)
-        During guided decoding, the JSON structure may not be closed properly.
+        """"""Fix incomplete JSON responses from vLLM guided decoding.
+
+        When using guided decoding with vLLM, sometimes the JSON response is incomplete
+        and missing the closing brace. This method adds the closing brace if needed.
+        (https://github.com/vllm-project/vllm/issues/8350)
 
         Args:
-            response_message (str): The response message to fix
+            response_message (str): The potentially incomplete JSON response
 
         Returns:
-            str: The fixed response message
+            str: The JSON response with proper closing brace
         """"""
         if not response_message.endswith(""}""):
             response_message += ""}""
         return response_message
 
-    def process_requests(
-        self, requests: list[APIRequest], status_tracker: OfflineStatusTracker
-    ) -> list[GenericResponse]:
-        """"""Process a list of generic requests using the VLLM model.
+    def process_requests(self, requests: list[APIRequest], status_tracker: OfflineStatusTracker) -> list[GenericResponse]:
+        """"""Process a list of API requests using the VLLM model.
 
         Args:
-            generic_requests (list[GenericRequest]): List of generic requests to process
+            requests (list[APIRequest]): List of API requests to process
             status_tracker (OfflineStatusTracker): Status tracker for the request
 
         Returns:
@@ -189,10 +181,7 @@ def process_requests(
             guided_decoding_params = GuidedDecodingParams(json=response_format)
         else:
             if response_format is not None:
-                logger.warning(
-                    f""Model {self.model} does not support structured output via guided decoding, ""
-                    f""response_format: {response_format}""
-                )
+                logger.warning(f""Model {self.model} does not support structured output via guided decoding, "" f""response_format: {response_format}"")
 
         sampling_params = {
             ""guided_decoding"": guided_decoding_params,
@@ -201,9 +190,7 @@ def process_requests(
             **self.generation_params,
         }
 
-        formatted_prompts = self.format_prompts(
-            [request.generic_request.messages for request in requests]
-        )
+        formatted_prompts = self.format_prompts([request.generic_request.messages for request in requests])
 
         completions = self.model_class.generate(
             formatted_prompts,