@@ -214,10 +214,27 @@ def cleanup_expired_cache(self, max_age_days: int = 7) -> None:
         """"""
         Removes cache entries older than the specified number of days.
         
+        This method helps maintain the cache size and ensures that only recent
+        responses are kept, which is important for keeping the cache relevant
+        and preventing it from growing too large over time.
+        
         Args:
             max_age_days: Maximum age of cache entries in days. Defaults to 7.
                           If set to 0, all entries will be deleted.
+                          Must be a non-negative integer.
+                          
+        Raises:
+            ValueError: If max_age_days is not a non-negative integer.
         """"""
+        if not isinstance(max_age_days, int) or max_age_days < 0:
+            error_msg = ""max_age_days must be a non-negative integer""
+            self._printer.print(
+                content=f""LLM RESPONSE CACHE ERROR: {error_msg}"",
+                color=""red"",
+            )
+            logger.error(error_msg)
+            raise ValueError(error_msg)
+            
         try:
             conn = self._get_connection()
             cursor = conn.cursor()