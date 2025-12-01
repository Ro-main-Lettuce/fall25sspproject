@@ -19,10 +19,11 @@
 from functools import lru_cache
 from pathlib import Path
 
-import pendulum
 import structlog
 import ulid
 
+from airbyte_cdk.utils.datetime_helpers import ab_datetime_now
+
 
 def _str_to_bool(value: str) -> bool:
     """"""Convert a string value of an environment values to a boolean value.""""""
@@ -60,6 +61,7 @@ def warn_once(
 
     if not with_stack:
         stacklevel = 0
+
     if with_stack is True:
         stacklevel = 2
 
@@ -139,7 +141,7 @@ def get_global_file_logger() -> logging.Logger | None:
     for handler in logger.handlers:
         logger.removeHandler(handler)
 
-    yyyy_mm_dd: str = pendulum.now().format(""YYYY-MM-DD"")
+    yyyy_mm_dd: str = ab_datetime_now().strftime(""%Y-%m-%d"")
     folder = AIRBYTE_LOGGING_ROOT / yyyy_mm_dd
     try:
         folder.mkdir(parents=True, exist_ok=True)