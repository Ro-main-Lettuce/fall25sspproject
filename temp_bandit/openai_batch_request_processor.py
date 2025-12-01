@@ -1,26 +1,17 @@
 import asyncio
-import datetime
 import json
 import logging
-from typing import Optional
 
 import litellm
 from openai import AsyncOpenAI, NotFoundError
 from openai.types.batch import Batch
 from openai.types.batch_request_counts import BatchRequestCounts
 from openai.types.file_object import FileObject
 
-from bespokelabs.curator.llm.prompt_formatter import PromptFormatter
-from bespokelabs.curator.request_processor.batch.base_batch_request_processor import (
-    BaseBatchRequestProcessor,
-)
+from bespokelabs.curator.request_processor.batch.base_batch_request_processor import BaseBatchRequestProcessor
 from bespokelabs.curator.request_processor.config import BatchRequestProcessorConfig
 from bespokelabs.curator.request_processor.openai_request_mixin import OpenAIRequestMixin
-from bespokelabs.curator.types.generic_batch import (
-    GenericBatch,
-    GenericBatchRequestCounts,
-    GenericBatchStatus,
-)
+from bespokelabs.curator.types.generic_batch import GenericBatch, GenericBatchRequestCounts, GenericBatchStatus
 from bespokelabs.curator.types.generic_request import GenericRequest
 from bespokelabs.curator.types.generic_response import GenericResponse
 from bespokelabs.curator.types.token_usage import TokenUsage
@@ -29,31 +20,42 @@
 
 
 class OpenAIBatchRequestProcessor(BaseBatchRequestProcessor, OpenAIRequestMixin):
+    """"""OpenAI-specific implementation of the BatchRequestProcessor.
+
+    This class handles batch processing of requests using OpenAI's API, including
+    file uploads, batch submissions, and result retrieval.
+    """"""
+
     def __init__(self, config: BatchRequestProcessorConfig) -> None:
+        """"""Initialize the OpenAIBatchRequestProcessor.""""""
         super().__init__(config)
         if self.config.base_url is None:
             self.client = AsyncOpenAI(max_retries=self.config.max_retries)
         else:
-            self.client = AsyncOpenAI(
-                max_retries=self.config.max_retries, base_url=self.config.base_url
-            )
+            self.client = AsyncOpenAI(max_retries=self.config.max_retries, base_url=self.config.base_url)
         self.web_dashboard = ""https://platform.openai.com/batches""
 
+    @property
+    def backend(self):
+        """"""Backend property.""""""
+        return ""openai""
+
     @property
     def max_requests_per_batch(self) -> int:
+        """"""The maximum number of requests that can be processed in a batch.""""""
         return 50_000
 
     @property
     def max_bytes_per_batch(self) -> int:
+        """"""The maximum number of bytes that can be processed in a batch.""""""
         return 200 * 1024 * 1024  # 200 MB
 
     @property
     def max_concurrent_batch_operations(self) -> int:
+        """"""The maximum number of concurrent batch operations.""""""
         return 100
 
-    def parse_api_specific_request_counts(
-        self, request_counts: BatchRequestCounts
-    ) -> GenericBatchRequestCounts:
+    def parse_api_specific_request_counts(self, request_counts: BatchRequestCounts) -> GenericBatchRequestCounts:
         """"""Convert OpenAI-specific request counts to generic format.
 
         Handles the following OpenAI request count statuses:
@@ -74,9 +76,7 @@ def parse_api_specific_request_counts(
             raw_request_counts_object=request_counts.model_dump(),
         )
 
-    def parse_api_specific_batch_object(
-        self, batch: Batch, request_file: str | None = None
-    ) -> GenericBatch:
+    def parse_api_specific_batch_object(self, batch: Batch, request_file: str | None = None) -> GenericBatch:
         """"""Convert an OpenAI batch object to generic format.
 
         Maps OpenAI-specific batch statuses and timing information to our
@@ -107,9 +107,7 @@ def parse_api_specific_batch_object(
         else:
             raise ValueError(f""Unknown batch status: {batch.status}"")
 
-        finished_at = (
-            batch.completed_at or batch.failed_at or batch.expired_at or batch.cancelled_at
-        )
+        finished_at = batch.completed_at or batch.failed_at or batch.expired_at or batch.cancelled_at
 
         return GenericBatch(
             request_file=batch.metadata[""request_file""],
@@ -168,9 +166,7 @@ def parse_api_specific_response(
                 completion_tokens=usage.get(""completion_tokens"", 0),
                 total_tokens=usage.get(""total_tokens"", 0),
             )
-            response_message, response_errors = self.prompt_formatter.parse_response_message(
-                response_message_raw
-            )
+            response_message, response_errors = self.prompt_formatter.parse_response_message(response_message_raw)
 
             cost = litellm.completion_cost(
                 model=self.config.model,
@@ -192,8 +188,7 @@ def parse_api_specific_response(
         )
 
     def create_api_specific_request_batch(self, generic_request: GenericRequest) -> dict:
-        """"""
-        Creates an API-specific request body from a generic request body.
+        """"""Creates an API-specific request body from a generic request body.
 
         This function transforms a GenericRequest into the format expected by OpenAI's batch API.
         It handles both standard requests and those with JSON schema response formats.
@@ -219,8 +214,7 @@ def create_api_specific_request_batch(self, generic_request: GenericRequest) ->
         return request
 
     async def upload_batch_file(self, file_content: bytes) -> FileObject:
-        """"""
-        Uploads a batch file to OpenAI and waits until ready.
+        """"""Uploads a batch file to OpenAI and waits until ready.
 
         Args:
             file_content (bytes): The encoded file content to upload
@@ -249,8 +243,7 @@ async def upload_batch_file(self, file_content: bytes) -> FileObject:
         return batch_file_upload
 
     async def create_batch(self, batch_file_id: str, metadata: dict) -> Batch:
-        """"""
-        Creates a batch job with OpenAI using an uploaded file.
+        """"""Creates a batch job with OpenAI using an uploaded file.
 
         Args:
             batch_file_id (str): ID of the uploaded file to use for the batch
@@ -276,8 +269,7 @@ async def create_batch(self, batch_file_id: str, metadata: dict) -> Batch:
         return batch
 
     async def submit_batch(self, requests: list[dict], metadata: dict) -> GenericBatch:
-        """"""
-        Handles the complete batch submission process.
+        """"""Handles the complete batch submission process.
 
         Args:
             requests (list[dict]): List of API-specific requests to submit
@@ -312,16 +304,12 @@ async def retrieve_batch(self, batch: GenericBatch) -> GenericBatch:
         try:
             batch = await self.client.batches.retrieve(batch.id)
         except NotFoundError:
-            logger.warning(
-                f""batch object {batch.id} not found. ""
-                f""Your API key (***{self.client.api_key[-4:]}) might not have access to this batch.""
-            )
+            logger.warning(f""batch object {batch.id} not found. "" f""Your API key (***{self.client.api_key[-4:]}) might not have access to this batch."")
             return None
         return self.parse_api_specific_batch_object(batch)
 
     async def delete_file(self, file_id: str, semaphore: asyncio.Semaphore):
-        """"""
-        Deletes a file from OpenAI's storage.
+        """"""Deletes a file from OpenAI's storage.
 
         Args:
             file_id (str): The ID of the file to delete
@@ -359,14 +347,15 @@ async def download_batch(self, batch: GenericBatch) -> list[dict] | None:
             - Handles file cleanup for failed/cancelled/expired batches
         """"""
         output_file_content = None
-        error_file_content = None  # TODO how should we use this?
+        error_file_content = None  # noqa: F841
         openai_batch = Batch.model_validate(batch.raw_batch)
         async with self.semaphore:
             # Completed batches have an output file
             if openai_batch.output_file_id:
                 output_file_content = await self.client.files.content(openai_batch.output_file_id)
             if openai_batch.error_file_id:
-                error_file_content = await self.client.files.content(openai_batch.error_file_id)
+                # TODO: Do we need to handle this?
+                error_file_content = await self.client.files.content(openai_batch.error_file_id)  # noqa: F841
 
             if openai_batch.status == ""completed"" and openai_batch.output_file_id:
                 logger.debug(f""Batch {batch.id} completed and downloaded"")