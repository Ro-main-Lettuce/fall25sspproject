@@ -52,7 +52,9 @@ def __init__(
         self._do_cleanup = cleanup
         self._active_batches: dict[str, BatchHandle] = {}
         self._completed_batches: dict[str, list[BatchHandle]] = defaultdict(list, {})
-        self._active_batches_lock = __import__('threading').Lock()  # Thread safety for concurrent access
+        self._active_batches_lock = __import__(
+            ""threading""
+        ).Lock()  # Thread safety for concurrent access
 
     def _get_new_cache_file_path(
         self,
@@ -98,7 +100,7 @@ def _flush_active_batch(
             del self._active_batches[stream_name]
 
             self._completed_batches[stream_name].append(batch_handle)
-            
+
         progress_tracker.log_batch_written(
             stream_name=stream_name,
             batch_size=batch_handle.record_count,
@@ -119,7 +121,7 @@ def _new_batch(
         with self._active_batches_lock:
             if stream_name in self._active_batches:
                 pass
-        
+
         if stream_name in self._active_batches:
             self._flush_active_batch(
                 stream_name=stream_name,
@@ -135,7 +137,7 @@ def _new_batch(
             files=[new_file_path],
             file_opener=self._open_new_file,
         )
-        
+
         with self._active_batches_lock:
             self._active_batches[stream_name] = batch_handle
         return batch_handle
@@ -162,7 +164,7 @@ def cleanup_all(self) -> None:
         """"""
         with self._active_batches_lock:
             active_batches = list(self._active_batches.values())
-            
+
         for batch_handle in active_batches:
             self._cleanup_batch(batch_handle)
 
@@ -185,7 +187,7 @@ def process_record_message(
         batch_handle: BatchHandle
         with self._active_batches_lock:
             has_active_batch = stream_name in self._active_batches
-            
+
         if not has_active_batch:
             batch_handle = self._new_batch(
                 stream_name=stream_name,
@@ -240,7 +242,7 @@ def flush_active_batches(
         """"""Flush active batches for all streams.""""""
         with self._active_batches_lock:
             streams = list(self._active_batches.keys())
-            
+
         for stream_name in streams:
             self._flush_active_batch(
                 stream_name=stream_name,