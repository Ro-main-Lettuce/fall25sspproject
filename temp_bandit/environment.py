@@ -10,7 +10,7 @@
 import multiprocessing
 import os
 import platform
-from collections.abc import Callable
+from collections.abc import Callable, Sequence
 from functools import lru_cache
 from pathlib import Path
 from typing import (
@@ -227,7 +227,7 @@ def interpret_env_var_value(
         return interpret_existing_path_env(value, field_name)
     if field_type is Plugin:
         return interpret_plugin_env(value, field_name)
-    if get_origin(field_type) is list:
+    if get_origin(field_type) in (list, Sequence):
         return [
             interpret_env_var_value(
                 v,