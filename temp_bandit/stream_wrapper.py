@@ -84,6 +84,10 @@ def __exit__(self, exc_type, exc_val, exc_tb):
         context_api.detach(self._token)
         return False
 
+    def __getattr__(self, name):
+        """"""Delegate attribute access to the original stream.""""""
+        return getattr(self._stream, name)
+
     def _process_chunk(self, chunk: Any) -> None:
         """"""Process a single chunk from the stream.
 
@@ -320,6 +324,10 @@ async def __aexit__(self, exc_type, exc_val, exc_tb):
         context_api.detach(self._token)
         return False
 
+    def __getattr__(self, name):
+        """"""Delegate attribute access to the original stream.""""""
+        return getattr(self._stream, name)
+
 
 @_with_tracer_wrapper
 def chat_completion_stream_wrapper(tracer, wrapped, instance, args, kwargs):