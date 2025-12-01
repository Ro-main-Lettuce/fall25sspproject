@@ -9,6 +9,7 @@
 # Global buffer to store logs
 _log_buffer = StringIO()
 
+print_logger = None
 
 def setup_print_logger() -> None:
     """"""
@@ -28,7 +29,8 @@ def setup_print_logger() -> None:
 
         # Ensure the new logger doesn't propagate to root
         buffer_logger.propagate = False
-
+    
+    global print_logger
     def print_logger(*args: Any, **kwargs: Any) -> None:
         """"""
         Custom print function that logs to buffer and console.