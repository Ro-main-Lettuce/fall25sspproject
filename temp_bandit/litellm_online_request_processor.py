@@ -7,10 +7,10 @@
 import litellm
 from pydantic import BaseModel
 
-from bespokelabs.curator.request_processor import APIRequest, BaseOnlineRequestProcessor
 from bespokelabs.curator.request_processor.config import OnlineRequestProcessorConfig
 from bespokelabs.curator.request_processor.event_loop import run_in_event_loop
-from bespokelabs.curator.status_tracker import OnlineStatusTracker
+from bespokelabs.curator.request_processor.online.base_online_request_processor import APIRequest, BaseOnlineRequestProcessor
+from bespokelabs.curator.status_tracker.online_status_tracker import OnlineStatusTracker
 from bespokelabs.curator.types.generic_request import GenericRequest
 from bespokelabs.curator.types.generic_response import GenericResponse, TokenUsage
 
@@ -38,13 +38,17 @@ class LiteLLMOnlineRequestProcessor(BaseOnlineRequestProcessor):
     """"""
 
     def __init__(self, config: OnlineRequestProcessorConfig):
+        """"""Initialize the LiteLLMOnlineRequestProcessor.""""""
         super().__init__(config)
         if self.config.base_url is not None:
             litellm.api_base = self.config.base_url
         self.client = instructor.from_litellm(litellm.acompletion)
-        self.header_based_max_requests_per_minute, self.header_based_max_tokens_per_minute = (
-            self.get_header_based_rate_limits()
-        )
+        self.header_based_max_requests_per_minute, self.header_based_max_tokens_per_minute = self.get_header_based_rate_limits()
+
+    @property
+    def backend(self):
+        """"""Backend property.""""""
+        return ""litellm""
 
     def check_structured_output_support(self):
         """"""Verify if the model supports structured output via instructor.
@@ -75,18 +79,14 @@ class User(BaseModel):
             )
             logger.info(f""Check instructor structure output response: {response}"")
             assert isinstance(response, User)
-            logger.info(
-                f""Model {self.config.model} supports structured output via instructor, response: {response}""
-            )
+            logger.info(f""Model {self.config.model} supports structured output via instructor, response: {response}"")
             return True
         except instructor.exceptions.InstructorRetryException as e:
             if ""litellm.AuthenticationError"" in str(e):
                 logger.warning(f""Please provide a valid API key for model {self.config.model}."")
                 raise e
             else:
-                logger.warning(
-                    f""Model {self.config.model} does not support structured output via instructor: {e} {type(e)} {e.__cause__}""
-                )
+                logger.warning(f""Model {self.config.model} does not support structured output via instructor: {e} {type(e)} {e.__cause__}"")
                 return False
 
     def estimate_output_tokens(self) -> int:
@@ -123,11 +123,10 @@ def estimate_total_tokens(self, messages: list) -> int:
         return input_tokens + output_tokens
 
     def test_call(self):
+        """"""Test call to get rate limits.""""""
         completion = litellm.completion(
             model=self.config.model,
-            messages=[
-                {""role"": ""user"", ""content"": ""hi""}
-            ],  # Some models (e.g. Claude) require an non-empty message to get rate limits.
+            messages=[{""role"": ""user"", ""content"": ""hi""}],  # Some models (e.g. Claude) require an non-empty message to get rate limits.
         )
         # Try the method of caculating cost
         try:
@@ -230,20 +229,18 @@ async def call_single_request(
         # Get response directly without extra logging
         try:
             if request.generic_request.response_format:
-                response, completion_obj = (
-                    await self.client.chat.completions.create_with_completion(
-                        **request.api_specific_request,
-                        response_model=request.prompt_formatter.response_format,
-                        timeout=self.config.request_timeout,
-                    )
-                )
-                response_message = (
-                    response.model_dump() if hasattr(response, ""model_dump"") else response
+                (
+                    response,
+                    completion_obj,
+                ) = await self.client.chat.completions.create_with_completion(
+                    **request.api_specific_request,
+                    response_model=request.prompt_formatter.response_format,
+                    timeout=self.config.request_timeout,
                 )
+                response_message = response.model_dump() if hasattr(response, ""model_dump"") else response
+                response_message = response.model_dump() if hasattr(response, ""model_dump"") else response
             else:
-                completion_obj = await litellm.acompletion(
-                    **request.api_specific_request, timeout=self.config.request_timeout
-                )
+                completion_obj = await litellm.acompletion(**request.api_specific_request, timeout=self.config.request_timeout)
                 response_message = completion_obj[""choices""][0][""message""][""content""]
         except litellm.RateLimitError as e:
             status_tracker.time_of_last_rate_limit_error = time.time()
@@ -265,15 +262,11 @@ async def call_single_request(
         finish_reason = completion_obj.choices[0].finish_reason
         invalid_finish_reasons = [""length"", ""content_filter""]
         if finish_reason in invalid_finish_reasons:
-            logger.debug(
-                f""Invalid finish_reason {finish_reason}. Raw response {completion_obj.model_dump()} for request {request.generic_request.messages}""
-            )
+            logger.debug(f""Invalid finish_reason {finish_reason}. Raw response {completion_obj.model_dump()} for request {request.generic_request.messages}"")
             raise ValueError(f""finish_reason was {finish_reason}"")
 
         if response_message is None:
-            raise ValueError(
-                f""response_message was None with raw response {completion_obj.model_dump()}""
-            )
+            raise ValueError(f""response_message was None with raw response {completion_obj.model_dump()}"")
 
         # Create and return response
         return GenericResponse(