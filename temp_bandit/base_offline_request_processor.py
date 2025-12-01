@@ -1,26 +1,36 @@
-from abc import ABC
-from dataclasses import dataclass, field
 import datetime
-from typing import Optional
+import json
 import logging
 import os
-import json
+import typing as t
+from abc import ABC
+from dataclasses import dataclass, field
 
-from bespokelabs.curator.dataset import Dataset
-from bespokelabs.curator.request_processor.base_request_processor import BaseRequestProcessor
 from bespokelabs.curator.llm.prompt_formatter import PromptFormatter
+from bespokelabs.curator.request_processor.base_request_processor import BaseRequestProcessor
+from bespokelabs.curator.request_processor.config import OfflineRequestProcessorConfig
 from bespokelabs.curator.types.generic_request import GenericRequest
 from bespokelabs.curator.types.generic_response import GenericResponse
-from bespokelabs.curator.request_processor.config import OfflineRequestProcessorConfig
-from bespokelabs.curator.status_tracker import OfflineStatusTracker
 
 logger = logging.getLogger(__name__)
 logger.setLevel(logging.INFO)
 
+if t.TYPE_CHECKING:
+    from bespokelabs.curator.status_tracker.offline_status_tracker import OfflineStatusTracker
+
 
 @dataclass
 class APIRequest:
-    """"""Stores an API request's inputs, outputs, and other metadata.""""""
+    """"""Stores an API request's inputs, outputs, and other metadata.
+
+    Attributes:
+        task_id: Unique identifier for this request
+        generic_request: The generic request object containing prompt and parameters
+        api_specific_request: Request formatted for the specific API being used
+        result: List to store results from the API
+        prompt_formatter: Formatter used to create prompts
+        created_at: Timestamp when request was created
+    """"""
 
     task_id: int
     generic_request: GenericRequest
@@ -31,14 +41,24 @@ class APIRequest:
 
 
 class BaseOfflineRequestProcessor(BaseRequestProcessor, ABC):
-    """"""
-    Base class for offline request processors.
+    """"""Base class for offline request processors.
+
+    Provides core functionality for processing requests through offline models, including:
+    - Model loading and configuration
+    - Request processing and response generation
+    - File handling and resumption of interrupted processing
 
     Args:
-        config (OfflineRequestProcessorConfig): Configuration for the request processor
+        config (OfflineRequestProcessorConfig): Configuration for the request processor containing
+            model parameters and processing settings
     """"""
 
     def __init__(self, config: OfflineRequestProcessorConfig):
+        """"""Initialize the offline request processor.
+
+        Args:
+            config: Configuration object containing model and processing parameters
+        """"""
         super().__init__(config)
         self.model: str = config.model
         self.max_model_length: int = config.max_model_length
@@ -50,23 +70,46 @@ def __init__(self, config: OfflineRequestProcessorConfig):
         self.batch_size: int = config.batch_size
         self.generation_params = config.generation_params
 
+    @property
+    def backend(self):
+        """"""Backend property.""""""
+        return ""base""
+
     def load_offline_model(self):
-        """"""Load the offline model.""""""
+        """"""Load the offline model into memory.
+
+        Should be implemented by subclasses to handle specific model loading logic.
+        """"""
         pass
 
     def destroy(self) -> None:
-        """"""Destroy the model.""""""
+        """"""Clean up model resources.
+
+        Should be implemented by subclasses to handle model cleanup.
+        """"""
         pass
 
-    def process_requests(
-        self, requests: list[APIRequest], status_tracker: OfflineStatusTracker
-    ) -> list[GenericResponse]:
+    def process_requests(self, requests: list[APIRequest], status_tracker: ""OfflineStatusTracker"") -> list[GenericResponse]:
+        """"""Process a batch of requests through the model.
+
+        Args:
+            requests: List of API requests to process
+            status_tracker: Tracker to monitor processing status
+
+        Returns:
+            List of responses from the model
+        """"""
         pass
 
     def requests_to_responses(
         self,
         generic_request_files: list[str],
     ) -> None:
+        """"""Process multiple request files and generate corresponding response files.
+
+        Args:
+            generic_request_files: List of paths to request files to process
+        """"""
         for request_file in generic_request_files:
             response_file = request_file.replace(""requests_"", ""responses_"")
             self.process_requests_from_file(
@@ -82,6 +125,23 @@ def process_requests_from_file(
         resume: bool,
         resume_no_retry: bool = False,
     ) -> None:
+        """"""Process requests from a file and save responses.
+
+        Handles resuming interrupted processing and retrying failed requests.
+        Creates response files with results from model inference.
+
+        Args:
+            generic_request_filepath: Path to file containing requests
+            save_filepath: Path to save response file
+            resume: Whether to resume processing from previous state
+            resume_no_retry: Whether to skip retrying failed requests when resuming
+
+        Side Effects:
+            - Creates/updates response file with model outputs
+            - Logs progress and completion status
+            - May prompt user for confirmation on file overwrite
+        """"""
+        from bespokelabs.curator.status_tracker.offline_status_tracker import OfflineStatusTracker
 
         status_tracker = OfflineStatusTracker()
 
@@ -90,15 +150,11 @@ def process_requests_from_file(
         if os.path.exists(save_filepath):
             if resume:
                 logger.info(f""Resuming progress by reading existing file: {save_filepath}"")
-                logger.debug(
-                    f""Removing all failed requests from {save_filepath} so they can be retried""
-                )
+                logger.debug(f""Removing all failed requests from {save_filepath} so they can be retried"")
                 temp_filepath = f""{save_filepath}.temp""
                 num_previously_failed_requests = 0
 
-                with open(save_filepath, ""r"") as input_file, open(
-                    temp_filepath, ""w""
-                ) as output_file:
+                with open(save_filepath, ""r"") as input_file, open(temp_filepath, ""w"") as output_file:
                     for line in input_file:
                         response = GenericResponse.model_validate_json(line)
                         if response.response_errors:
@@ -116,17 +172,12 @@ def process_requests_from_file(
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
@@ -140,10 +191,7 @@ def process_requests_from_file(
                             num_previously_failed_requests += 1
                         completed_request_ids.add(response.generic_request.original_row_idx)
 
-                logger.info(
-                    f""Found {len(completed_request_ids)} total requests and ""
-                    f""{num_previously_failed_requests} previously failed requests""
-                )
+                logger.info(f""Found {len(completed_request_ids)} total requests and "" f""{num_previously_failed_requests} previously failed requests"")
                 logger.info(""Remaining requests will now be processed."")
 
             else: