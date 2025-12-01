@@ -1,5 +1,4 @@
 import asyncio
-import datetime
 import json
 import logging
 import os
@@ -8,17 +7,11 @@
 
 from tqdm import tqdm
 
-from bespokelabs.curator.dataset import Dataset
-from bespokelabs.curator.llm.prompt_formatter import PromptFormatter
 from bespokelabs.curator.request_processor.base_request_processor import BaseRequestProcessor
 from bespokelabs.curator.request_processor.config import BatchRequestProcessorConfig
 from bespokelabs.curator.request_processor.event_loop import run_in_event_loop
 from bespokelabs.curator.status_tracker.batch_status_tracker import BatchStatusTracker
-from bespokelabs.curator.types.generic_batch import (
-    GenericBatch,
-    GenericBatchRequestCounts,
-    GenericBatchStatus,
-)
+from bespokelabs.curator.types.generic_batch import GenericBatch, GenericBatchRequestCounts, GenericBatchStatus
 from bespokelabs.curator.types.generic_request import GenericRequest
 from bespokelabs.curator.types.generic_response import GenericResponse
 
@@ -60,6 +53,11 @@ def __init__(self, config: BatchRequestProcessorConfig):
         """"""
         super().__init__(config)
 
+    @property
+    def backend(self) -> str:
+        """"""Backend property.""""""
+        return ""base""
+
     def requests_to_responses(self, generic_request_files: list[str]) -> None:
         """"""Process multiple request files using batch API operations.
 
@@ -95,29 +93,9 @@ def requests_to_responses(self, generic_request_files: list[str]) -> None:
         self.request_pbar: tqdm | None = None
 
         run_in_event_loop(self.submit_batches_from_request_files(generic_request_files))
-        logger.info(
-            f""Submitted batches. These can be viewed in the web dashboard: {self.web_dashboard}""
-        )
+        logger.info(f""Submitted batches. These can be viewed in the web dashboard: {self.web_dashboard}"")
         run_in_event_loop(self.poll_and_process_batches())
 
-    def cancel_batches(self) -> Dataset:
-        """"""Cancel all submitted batches and exit.
-
-        Initiates cancellation of all submitted batches and exits the program
-        after attempting cancellation.
-
-        Returns:
-            Dataset: Not actually returned due to program exit.
-
-        Side Effects:
-            - Attempts to cancel all submitted batches
-            - Logs warning about cancellation
-            - Forces program exit with status code 1
-        """"""
-        run_in_event_loop(self.cancel_batches())
-        logger.warning(""Exiting program after batch cancellation."")
-        os._exit(1)
-
     @property
     @abstractmethod
     def max_requests_per_batch(self) -> int:
@@ -167,9 +145,7 @@ def max_concurrent_batch_operations(self) -> int:
         pass
 
     @abstractmethod
-    async def submit_batch(
-        self, requests: list[dict], metadata: Optional[dict] = None
-    ) -> GenericBatch:
+    async def submit_batch(self, requests: list[dict], metadata: Optional[dict] = None) -> GenericBatch:
         """"""Submit a batch of requests to the API provider.
 
         Args:
@@ -267,9 +243,7 @@ def create_api_specific_request_batch(self, generic_request: GenericRequest) ->
         pass
 
     @abstractmethod
-    def parse_api_specific_batch_object(
-        self, batch: object, request_file: str | None = None
-    ) -> GenericBatch:
+    def parse_api_specific_batch_object(self, batch: object, request_file: str | None = None) -> GenericBatch:
         """"""Convert API-specific batch object to generic format.
 
         Args:
@@ -282,9 +256,7 @@ def parse_api_specific_batch_object(
         pass
 
     @abstractmethod
-    def parse_api_specific_request_counts(
-        self, request_counts: object
-    ) -> GenericBatchRequestCounts:
+    def parse_api_specific_request_counts(self, request_counts: object) -> GenericBatchRequestCounts:
         """"""Convert API-specific request counts to generic format.
 
         Args:
@@ -353,9 +325,7 @@ def create_batch_file(self, api_specific_requests: list[dict]) -> str:
         # Join requests with newlines and encode to bytes for upload
         file_content = ""
"".join(json.dumps(r) for r in api_specific_requests).encode()
         file_content_size = len(file_content)
-        logger.debug(
-            f""Batch file content size: {file_content_size / (1024*1024):.2f} MB ({file_content_size:,} bytes)""
-        )
+        logger.debug(f""Batch file content size: {file_content_size / (1024*1024):.2f} MB ({file_content_size:,} bytes)"")
         if file_content_size > self.max_bytes_per_batch:
             raise ValueError(
                 f""Batch file content size {file_content_size:,} bytes ""
@@ -414,9 +384,7 @@ def requests_from_generic_request_file(self, request_file: str) -> list[dict]:
 
         return api_specific_requests
 
-    def generic_response_file_from_responses(
-        self, responses: list[dict], batch: GenericBatch
-    ) -> str | None:
+    def generic_response_file_from_responses(self, responses: list[dict], batch: GenericBatch) -> str | None:
         """"""Process API responses and create generic response file.
 
         Converts API-specific responses to GenericResponse objects and writes them
@@ -442,7 +410,7 @@ def generic_response_file_from_responses(
         response_filename = request_filename.replace(""requests_"", ""responses_"")
         response_file = os.path.join(request_dir, response_filename)
         generic_request_map = {}
-        batch_created_at = batch.created_at
+        # batch_created_at = batch.created_at
         with open(request_file, ""r"") as f:
             for line in f:
                 generic_request = GenericRequest.model_validate_json(line)
@@ -452,9 +420,7 @@ def generic_response_file_from_responses(
             for raw_response in responses:
                 request_idx = int(raw_response[""custom_id""])
                 generic_request = generic_request_map[request_idx]
-                generic_response = self.parse_api_specific_response(
-                    raw_response, generic_request, batch
-                )
+                generic_response = self.parse_api_specific_response(raw_response, generic_request, batch)
                 json.dump(generic_response.model_dump(), f, default=str)
                 f.write(""
"")
 
@@ -481,9 +447,7 @@ async def submit_batches_from_request_files(
         if self.tracker.n_submitted_batches > 0:
             n_remaining = self.tracker.n_total_batches - self.tracker.n_downloaded_batches
             n_submitted = self.tracker.n_submitted_batches + self.tracker.n_finished_batches
-            logger.info(
-                f""{n_submitted:,} out of {n_remaining:,} remaining batches previously submitted.""
-            )
+            logger.info(f""{n_submitted:,} out of {n_remaining:,} remaining batches previously submitted."")
         # exit early
         if self.tracker.n_unsubmitted_request_files == 0:
             return
@@ -495,9 +459,7 @@ async def submit_batches_from_request_files(
             unit=""batch"",
             initial=self.tracker.n_submitted_finished_or_downloaded_batches,
         )
-        tasks = [
-            self.submit_batch_from_request_file(f) for f in self.tracker.unsubmitted_request_files
-        ]
+        tasks = [self.submit_batch_from_request_file(f) for f in self.tracker.unsubmitted_request_files]
         await asyncio.gather(*tasks)
         self.batch_submit_pbar.close()
         assert self.tracker.unsubmitted_request_files == set()
@@ -571,20 +533,15 @@ async def poll_and_process_batches(self) -> None:
         all_response_files = []
         while self.tracker.n_submitted_batches + self.tracker.n_finished_batches > 0:
             # check batch status also updates the tracker
-            status_tasks = [
-                self.check_batch_status(batch) for batch in self.tracker.submitted_batches.values()
-            ]
+            status_tasks = [self.check_batch_status(batch) for batch in self.tracker.submitted_batches.values()]
             await asyncio.gather(*status_tasks)
             await self.update_batch_objects_file()
 
             # update progress bari
             self.request_pbar.n = self.tracker.n_finished_or_downloaded_requests
             self.request_pbar.refresh()
 
-            download_tasks = [
-                self.download_batch_to_response_file(batch)
-                for batch in self.tracker.finished_batches.values()
-            ]
+            download_tasks = [self.download_batch_to_response_file(batch) for batch in self.tracker.finished_batches.values()]
             # Failed downloads return None and print any errors that occurred
             all_response_files.extend(await asyncio.gather(*download_tasks))
             if self.tracker.n_finished_or_downloaded_requests < self.tracker.n_total_requests:
@@ -598,10 +555,7 @@ async def poll_and_process_batches(self) -> None:
         self.request_pbar.close()
         response_files = filter(None, all_response_files)
         if self.tracker.n_downloaded_batches == 0 or not response_files:
-            raise RuntimeError(
-                ""None of the submitted batches completed successfully. ""
-                f""Please check the logs above and {self.web_dashboard} for errors.""
-            )
+            raise RuntimeError(""None of the submitted batches completed successfully. "" f""Please check the logs above and {self.web_dashboard} for errors."")
 
     async def download_batch_to_response_file(self, batch: GenericBatch) -> str | None:
         """"""Download and process completed batch results.
@@ -660,4 +614,4 @@ async def cancel_batches(self):
             logger.warning(""No batches to be cancelled, but cancel_batches=True."")
             return
         tasks = [self.cancel_batch(batch) for batch in self.tracker.submitted_batches.values()]
-        results = await asyncio.gather(*tasks)
+        await asyncio.gather(*tasks)