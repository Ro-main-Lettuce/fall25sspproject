@@ -1,3 +1,9 @@
+""""""Base class for online request processors that make real-time API calls.
+
+This module provides the core functionality for making API requests in real-time,
+handling rate limiting, retries, and parallel processing.
+""""""
+
 import asyncio
 import datetime
 import json
@@ -12,7 +18,6 @@
 import litellm
 from tqdm import tqdm
 
-from bespokelabs.curator.dataset import Dataset
 from bespokelabs.curator.llm.prompt_formatter import PromptFormatter
 from bespokelabs.curator.request_processor.base_request_processor import BaseRequestProcessor
 from bespokelabs.curator.request_processor.config import OnlineRequestProcessorConfig
@@ -26,7 +31,17 @@
 
 @dataclass
 class APIRequest:
-    """"""Stores an API request's inputs, outputs, and other metadata.""""""
+    """"""Stores an API request's inputs, outputs, and other metadata.
+
+    Attributes:
+        task_id: Unique identifier for the request
+        generic_request: The generic request object to be processed
+        api_specific_request: The request formatted for the specific API
+        attempts_left: Number of retry attempts remaining
+        result: List to store results/errors from attempts
+        prompt_formatter: Formatter for prompts and responses
+        created_at: Timestamp when request was created
+    """"""
 
     task_id: int
     generic_request: GenericRequest
@@ -38,9 +53,17 @@ class APIRequest:
 
 
 class BaseOnlineRequestProcessor(BaseRequestProcessor, ABC):
-    """"""Abstract base class for online request processors that make real-time API calls.""""""
+    """"""Abstract base class for online request processors that make real-time API calls.
+
+    This class handles rate limiting, retries, parallel processing and other common
+    functionality needed for making real-time API requests.
+
+    Args:
+        config: Configuration object containing settings for the request processor
+    """"""
 
     def __init__(self, config: OnlineRequestProcessorConfig):
+        """"""Initialize the BaseOnlineRequestProcessor.""""""
         super().__init__(config)
         self.manual_max_requests_per_minute = config.max_requests_per_minute
         self.manual_max_tokens_per_minute = config.max_tokens_per_minute
@@ -49,17 +72,23 @@ def __init__(self, config: OnlineRequestProcessorConfig):
         self.header_based_max_requests_per_minute = None
         self.header_based_max_tokens_per_minute = None
 
+    @property
+    def backend(self) -> str:
+        """"""Backend property.""""""
+        return ""base""
+
     @property
     def max_requests_per_minute(self) -> int:
+        """"""Gets the maximum requests per minute rate limit.
+
+        Returns the manually set limit if available, falls back to header-based limit,
+        or uses default value as last resort.
+        """"""
         if self.manual_max_requests_per_minute:
-            logger.info(
-                f""Manually set max_requests_per_minute to {self.manual_max_requests_per_minute}""
-            )
+            logger.info(f""Manually set max_requests_per_minute to {self.manual_max_requests_per_minute}"")
             return self.manual_max_requests_per_minute
         elif self.header_based_max_requests_per_minute:
-            logger.info(
-                f""Automatically set max_requests_per_minute to {self.header_based_max_requests_per_minute}""
-            )
+            logger.info(f""Automatically set max_requests_per_minute to {self.header_based_max_requests_per_minute}"")
             return self.header_based_max_requests_per_minute
         else:
             logger.warning(
@@ -69,15 +98,16 @@ def max_requests_per_minute(self) -> int:
 
     @property
     def max_tokens_per_minute(self) -> int:
+        """"""Gets the maximum tokens per minute rate limit.
+
+        Returns the manually set limit if available, falls back to header-based limit,
+        or uses default value as last resort.
+        """"""
         if self.manual_max_tokens_per_minute:
-            logger.info(
-                f""Manually set max_tokens_per_minute to {self.manual_max_tokens_per_minute}""
-            )
+            logger.info(f""Manually set max_tokens_per_minute to {self.manual_max_tokens_per_minute}"")
             return self.manual_max_tokens_per_minute
         elif self.header_based_max_tokens_per_minute:
-            logger.info(
-                f""Automatically set max_tokens_per_minute to {self.header_based_max_tokens_per_minute}""
-            )
+            logger.info(f""Automatically set max_tokens_per_minute to {self.header_based_max_tokens_per_minute}"")
             return self.header_based_max_tokens_per_minute
         else:
             logger.warning(
@@ -87,31 +117,64 @@ def max_tokens_per_minute(self) -> int:
 
     @abstractmethod
     def estimate_total_tokens(self, messages: list) -> int:
-        """"""Estimate total tokens for a request""""""
+        """"""Estimate total tokens for a request.
+
+        Args:
+            messages: List of messages to estimate token count for
+
+        Returns:
+            Estimated total number of tokens
+        """"""
         pass
 
     @abstractmethod
     def estimate_output_tokens(self) -> int:
-        """"""Estimate output tokens for a request""""""
+        """"""Estimate output tokens for a request.
+
+        Returns:
+            Estimated number of output tokens
+        """"""
         pass
 
     @abstractmethod
     def create_api_specific_request_online(self, generic_request: GenericRequest) -> dict:
-        """"""Create an API-specific request body from a generic request body.""""""
+        """"""Create an API-specific request body from a generic request body.
+
+        Args:
+            generic_request: The generic request to convert
+
+        Returns:
+            API-specific request dictionary
+        """"""
         pass
 
     def completion_cost(self, response):
+        """"""Calculate the cost of a completion response using litellm.
+
+        Args:
+            response: The completion response to calculate cost for
+
+        Returns:
+            Calculated cost of the completion
+        """"""
         # Calculate cost using litellm
         try:
             cost = litellm.completion_cost(completion_response=response)
-        except Exception as e:
+        except Exception:
             # We should ideally not catch a catch-all exception here. But litellm is not throwing any specific error.
             cost = 0
 
+        return cost
+
     def requests_to_responses(
         self,
         generic_request_files: list[str],
     ) -> None:
+        """"""Process multiple request files and generate corresponding response files.
+
+        Args:
+            generic_request_files: List of request files to process
+        """"""
         for request_file in generic_request_files:
             response_file = request_file.replace(""requests_"", ""responses_"")
             run_in_event_loop(
@@ -123,6 +186,11 @@ def requests_to_responses(
             )
 
     async def cool_down_if_rate_limit_error(self, status_tracker: OnlineStatusTracker) -> None:
+        """"""Pause processing if a rate limit error is detected.
+
+        Args:
+            status_tracker: Tracker containing rate limit status
+        """"""
         seconds_to_pause_on_rate_limit = self.config.seconds_to_pause_on_rate_limit
         seconds_since_rate_limit_error = time.time() - status_tracker.time_of_last_rate_limit_error
         remaining_seconds_to_pause = seconds_to_pause_on_rate_limit - seconds_since_rate_limit_error
@@ -137,8 +205,14 @@ async def process_requests_from_file(
         resume: bool,
         resume_no_retry: bool = False,
     ) -> None:
-        """"""Processes API requests in parallel, throttling to stay under rate limits.""""""
+        """"""Processes API requests in parallel, throttling to stay under rate limits.
 
+        Args:
+            generic_request_filepath: Path to file containing requests
+            save_filepath: Path to save responses
+            resume: Whether to resume from previous progress
+            resume_no_retry: Whether to skip retrying failed requests when resuming
+        """"""
         # Initialize trackers
         queue_of_requests_to_retry: asyncio.Queue[APIRequest] = asyncio.Queue()
         status_tracker = OnlineStatusTracker()
@@ -152,15 +226,11 @@ async def process_requests_from_file(
         if os.path.exists(save_filepath):
             if resume:
                 logger.info(f""Resuming progress by reading existing file: {save_filepath}"")
-                logger.debug(
-                    f""Removing all failed requests from {save_filepath} so they can be retried""
-                )
+                logger.debug(f""Removing all failed requests from {save_filepath} so they can be retried"")
                 temp_filepath = save_filepath + "".temp""  # This is a file extension, not a path join
                 num_previously_failed_requests = 0
 
-                with open(save_filepath, ""r"") as input_file, open(
-                    temp_filepath, ""w""
-                ) as output_file:
+                with open(save_filepath, ""r"") as input_file, open(temp_filepath, ""w"") as output_file:
                     for line in input_file:
                         response = GenericResponse.model_validate_json(line)
                         if response.response_errors:
@@ -178,17 +248,12 @@ async def process_requests_from_file(
                             completed_request_ids.add(response.generic_request.original_row_idx)
                             output_file.write(line)
 
-                logger.info(
-                    f""Found {len(completed_request_ids)} completed requests and ""
-                    f""{num_previously_failed_requests} previously failed requests""
-                )
+                logger.info(f""Found {len(completed_request_ids)} completed requests and "" f""{num_previously_failed_requests} previously failed requests"")
                 logger.info(""Failed requests and remaining requests will now be processed."")
                 os.replace(temp_filepath, save_filepath)
 
             elif resume_no_retry:
-                logger.warning(
-                    f""Resuming progress from existing file: {save_filepath}, without retrying failed requests""
-                )
+                logger.warning(f""Resuming progress from existing file: {save_filepath}, without retrying failed requests"")
                 num_previously_failed_requests = 0
 
                 with open(save_filepath, ""r"") as input_file:
@@ -202,10 +267,7 @@ async def process_requests_from_file(
                             num_previously_failed_requests += 1
                         completed_request_ids.add(response.generic_request.original_row_idx)
 
-                logger.info(
-                    f""Found {len(completed_request_ids)} total requests and ""
-                    f""{num_previously_failed_requests} previously failed requests""
-                )
+                logger.info(f""Found {len(completed_request_ids)} total requests and "" f""{num_previously_failed_requests} previously failed requests"")
                 logger.info(""Remaining requests will now be processed."")
 
             else:
@@ -244,9 +306,7 @@ async def process_requests_from_file(
                     request = APIRequest(
                         task_id=status_tracker.num_tasks_started,
                         generic_request=generic_request,
-                        api_specific_request=self.create_api_specific_request_online(
-                            generic_request
-                        ),
+                        api_specific_request=self.create_api_specific_request_online(generic_request),
                         attempts_left=self.config.max_retries,
                         prompt_formatter=self.prompt_formatter,
                     )
@@ -287,9 +347,7 @@ async def process_requests_from_file(
                 # Process new items from the queue if we have capacity
                 if not queue_of_requests_to_retry.empty():
                     retry_request = await queue_of_requests_to_retry.get()
-                    token_estimate = self.estimate_total_tokens(
-                        retry_request.generic_request.messages
-                    )
+                    token_estimate = self.estimate_total_tokens(retry_request.generic_request.messages)
                     attempt_number = self.config.max_retries - retry_request.attempts_left
                     logger.debug(
                         f""Retrying request {retry_request.task_id} ""
@@ -326,10 +384,7 @@ async def process_requests_from_file(
         logger.info(f""Status tracker: {status_tracker}"")
 
         if status_tracker.num_tasks_failed > 0:
-            logger.warning(
-                f""{status_tracker.num_tasks_failed} / {status_tracker.num_tasks_started} ""
-                f""requests failed. Errors logged to {save_filepath}.""
-            )
+            logger.warning(f""{status_tracker.num_tasks_failed} / {status_tracker.num_tasks_started} "" f""requests failed. Errors logged to {save_filepath}."")
 
     async def handle_single_request_with_retries(
         self,
@@ -345,11 +400,11 @@ async def handle_single_request_with_retries(
         while delegating the actual API call to call_single_request.
 
         Args:
-            request (APIRequest): The request to process
-            session (aiohttp.ClientSession): Async HTTP session
-            retry_queue (asyncio.Queue): Queue for failed requests
-            save_filepath (str): Path to save responses
-            status_tracker (OnlineStatusTracker): Tracks request status
+            request: The request to process
+            session: Async HTTP session
+            retry_queue: Queue for failed requests
+            save_filepath: Path to save responses
+            status_tracker: Tracks request status
         """"""
         try:
             generic_response = await self.call_single_request(
@@ -411,17 +466,22 @@ async def call_single_request(
         without handling retries or errors.
 
         Args:
-            request (APIRequest): Request to process
-            session (aiohttp.ClientSession): Async HTTP session
-            status_tracker (OnlineStatusTracker): Tracks request status
+            request: Request to process
+            session: Async HTTP session
+            status_tracker: Tracks request status
 
         Returns:
-            GenericResponse: The response from the API call
+            The response from the API call
         """"""
         pass
 
     async def append_generic_response(self, data: GenericResponse, filename: str) -> None:
-        """"""Append a response to a jsonl file with async file operations.""""""
+        """"""Append a response to a jsonl file with async file operations.
+
+        Args:
+            data: Response data to append
+            filename: File to append to
+        """"""
         json_string = json.dumps(data.model_dump(), default=str)
         async with aiofiles.open(filename, ""a"") as f:
             await f.write(json_string + ""
"")