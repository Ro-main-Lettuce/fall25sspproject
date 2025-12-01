@@ -9,6 +9,7 @@
 from typing import Any, Generic
 import json
 import os
+import io
 from .models import BatchResult, BatchSuccess, BatchError, BatchJobInfo, T
 from .request import BatchRequest
 from .providers import get_provider
@@ -36,55 +37,79 @@ def __init__(self, model: str, response_model: type[T]):
     def create_batch_from_messages(
         self,
         messages_list: list[list[dict[str, Any]]],
-        file_path: str,
+        file_path: str | None = None,
         max_tokens: int | None = 1000,
         temperature: float | None = 0.1,
-    ) -> str:
+    ) -> str | io.BytesIO:
         """"""Create batch file from list of message conversations
 
         Args:
             messages_list: List of message conversations, each as a list of message dicts
-            file_path: Path to save the batch request file
+            file_path: Path to save the batch request file. If None, returns BytesIO buffer
             max_tokens: Maximum tokens per request
             temperature: Temperature for generation
 
         Returns:
-            The file path where the batch was saved
+            The file path where the batch was saved, or BytesIO buffer if file_path is None
         """"""
-        # Remove existing file if it exists
-        if os.path.exists(file_path):
-            os.remove(file_path)
-
-        batch_requests = []
-        for i, messages in enumerate(messages_list):
-            batch_request = BatchRequest[self.response_model](
-                custom_id=f""request-{i}"",
-                messages=messages,
-                response_model=self.response_model,
-                model=self.model_name,
-                max_tokens=max_tokens,
-                temperature=temperature,
-            )
-            batch_request.save_to_file(file_path, self.provider_name)
-            batch_requests.append(batch_request)
-
-        print(f""Created batch file {file_path} with {len(batch_requests)} requests"")
-        return file_path
+        if file_path is not None:
+            if os.path.exists(file_path):
+                os.remove(file_path)
+
+            batch_requests = []
+            for i, messages in enumerate(messages_list):
+                batch_request = BatchRequest[self.response_model](
+                    custom_id=f""request-{i}"",
+                    messages=messages,
+                    response_model=self.response_model,
+                    model=self.model_name,
+                    max_tokens=max_tokens,
+                    temperature=temperature,
+                )
+                batch_request.save_to_file(file_path, self.provider_name)
+                batch_requests.append(batch_request)
+
+            print(f""Created batch file {file_path} with {len(batch_requests)} requests"")
+            return file_path
+        else:
+            # Create BytesIO buffer - caller is responsible for cleanup
+            buffer = io.BytesIO()
+            batch_requests = []
+            for i, messages in enumerate(messages_list):
+                batch_request = BatchRequest[self.response_model](
+                    custom_id=f""request-{i}"",
+                    messages=messages,
+                    response_model=self.response_model,
+                    model=self.model_name,
+                    max_tokens=max_tokens,
+                    temperature=temperature,
+                )
+                batch_request.save_to_file(buffer, self.provider_name)
+                batch_requests.append(batch_request)
+
+            print(f""Created batch buffer with {len(batch_requests)} requests"")
+            buffer.seek(0)  # Reset buffer position for reading
+            return buffer
 
     def submit_batch(
-        self, file_path: str, metadata: dict[str, Any] | None = None, **kwargs
+        self,
+        file_path_or_buffer: str | io.BytesIO,
+        metadata: dict[str, Any] | None = None,
+        **kwargs,
     ) -> str:
         """"""Submit batch job to the provider and return job ID
 
         Args:
-            file_path: Path to the batch request file
+            file_path_or_buffer: Path to the batch request file or BytesIO buffer
             metadata: Optional metadata to attach to the batch job
             **kwargs: Additional provider-specific arguments
         """"""
         if metadata is None:
             metadata = {""description"": ""Instructor batch job""}
 
-        return self.provider.submit_batch(file_path, metadata=metadata, **kwargs)
+        return self.provider.submit_batch(
+            file_path_or_buffer, metadata=metadata, **kwargs
+        )
 
     def get_batch_status(self, batch_id: str) -> dict[str, Any]:
         """"""Get batch job status from the provider""""""