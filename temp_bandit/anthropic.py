@@ -5,16 +5,23 @@
 """"""
 
 import json
-from typing import Any, Optional
+from typing import Any, Optional, Union
+import io
+import logging
 from .base import BatchProvider
 from ..models import BatchJobInfo
 
+logger = logging.getLogger(__name__)
+
 
 class AnthropicProvider(BatchProvider):
     """"""Anthropic batch processing provider""""""
 
     def submit_batch(
-        self, file_path: str, metadata: Optional[dict[str, Any]] = None, **kwargs
+        self,
+        file_path_or_buffer: Union[str, io.BytesIO],
+        metadata: Optional[dict[str, Any]] = None,
+        **kwargs,
     ) -> str:
         """"""Submit Anthropic batch job""""""
         _ = kwargs  # Unused but accepted for API consistency
@@ -30,19 +37,34 @@ def submit_batch(
                     f""Note: Anthropic batches don't support metadata. Ignoring: {metadata}""
                 )
 
-            # TODO: Remove beta fallback when stable API is available
+            # TODO(#batch-api-stable): Remove beta fallback when stable API is available
             try:
                 batches_client = client.messages.batches
             except AttributeError:
                 batches_client = client.beta.messages.batches
 
-            with open(file_path) as f:
-                requests = [json.loads(line) for line in f if line.strip()]
+            if isinstance(file_path_or_buffer, str):
+                with open(file_path_or_buffer) as f:
+                    requests = [json.loads(line) for line in f if line.strip()]
+            elif isinstance(file_path_or_buffer, io.BytesIO):
+                file_path_or_buffer.seek(0)
+                content = file_path_or_buffer.read().decode(""utf-8"")
+                requests = [
+                    json.loads(line) for line in content.split(""
"") if line.strip()
+                ]
+            else:
+                raise ValueError(
+                    f""Unsupported file_path_or_buffer type: {type(file_path_or_buffer)}""
+                )
 
             batch = batches_client.create(requests=requests)
             return batch.id
+        except (ValueError, TypeError) as e:
+            # Re-raise validation errors as-is
+            logger.error(f""Validation error in Anthropic batch submission: {e}"")
+            raise
         except Exception as e:
-            raise Exception(f""Failed to submit Anthropic batch: {e}"") from e
+            raise RuntimeError(f""Failed to submit Anthropic batch: {e}"") from e
 
     def get_status(self, batch_id: str) -> dict[str, Any]:
         """"""Get Anthropic batch status""""""
@@ -51,7 +73,7 @@ def get_status(self, batch_id: str) -> dict[str, Any]:
 
             client = anthropic.Anthropic()
 
-            # TODO: Remove beta fallback when stable API is available
+            # TODO(#batch-api-stable): Remove beta fallback when stable API is available
             try:
                 batches_client = client.messages.batches
             except AttributeError:
@@ -74,7 +96,7 @@ def retrieve_results(self, batch_id: str) -> str:
 
             client = anthropic.Anthropic()
 
-            # TODO: Remove beta fallback when stable API is available
+            # TODO(#batch-api-stable): Remove beta fallback when stable API is available
             try:
                 batches_client = client.messages.batches
             except AttributeError:
@@ -93,6 +115,18 @@ def retrieve_results(self, batch_id: str) -> str:
                     f""Batch not completed, status: {batch.processing_status}""
                 )
 
+            # Check if all requests failed
+            request_counts = getattr(batch, ""request_counts"", None)
+            if request_counts:
+                succeeded = getattr(request_counts, ""succeeded"", 0)
+                errored = getattr(request_counts, ""errored"", 0)
+                total = getattr(request_counts, ""total"", 0)
+
+                if errored > 0 and succeeded == 0:
+                    raise RuntimeError(
+                        f""All {total} batch requests failed. No results will be available.""
+                    )
+
             results = batches_client.results(batch_id)
             results_lines = []
             for result in results:
@@ -109,7 +143,7 @@ def download_results(self, batch_id: str, file_path: str) -> None:
 
             client = anthropic.Anthropic()
 
-            # TODO: Remove beta fallback when stable API is available
+            # TODO(#batch-api-stable): Remove beta fallback when stable API is available
             try:
                 batches_client = client.messages.batches
             except AttributeError:
@@ -128,6 +162,18 @@ def download_results(self, batch_id: str, file_path: str) -> None:
                     f""Batch not completed, status: {batch.processing_status}""
                 )
 
+            # Check if all requests failed
+            request_counts = getattr(batch, ""request_counts"", None)
+            if request_counts:
+                succeeded = getattr(request_counts, ""succeeded"", 0)
+                errored = getattr(request_counts, ""errored"", 0)
+                total = getattr(request_counts, ""total"", 0)
+
+                if errored > 0 and succeeded == 0:
+                    raise RuntimeError(
+                        f""All {total} batch requests failed. No results will be available.""
+                    )
+
             results = batches_client.results(batch_id)
             with open(file_path, ""w"") as f:
                 for result in results:
@@ -142,7 +188,7 @@ def cancel_batch(self, batch_id: str) -> dict[str, Any]:
 
             client = anthropic.Anthropic()
 
-            # TODO: Remove beta fallback when stable API is available
+            # TODO(#batch-api-stable): Remove beta fallback when stable API is available
             try:
                 batches_client = client.messages.batches
             except AttributeError:
@@ -160,7 +206,7 @@ def delete_batch(self, batch_id: str) -> dict[str, Any]:
 
             client = anthropic.Anthropic()
 
-            # TODO: Remove beta fallback when stable API is available
+            # TODO(#batch-api-stable): Remove beta fallback when stable API is available
             try:
                 batches_client = client.messages.batches
             except AttributeError:
@@ -182,7 +228,7 @@ def list_batches(self, limit: int = 10) -> list[BatchJobInfo]:
 
             client = anthropic.Anthropic()
 
-            # TODO: Remove beta fallback when stable API is available
+            # TODO(#batch-api-stable): Remove beta fallback when stable API is available
             try:
                 batches_client = client.messages.batches
             except AttributeError: