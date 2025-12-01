@@ -5,6 +5,7 @@
 import sys
 from typing import Any, Optional
 
+from ...import_utils import optional_import_block
 from ...tools import Tool
 from ..registry import register_interoperable_class
 
@@ -64,9 +65,10 @@ def get_unsupported_reason(cls) -> Optional[str]:
         if sys.version_info < (3, 9):
             return ""This submodule is only supported for Python versions 3.9 and above""
 
-        try:
+        with optional_import_block() as result:
             import langchain_core.tools  # noqa: F401
-        except ImportError:
+
+        if not result.is_successful:
             return (
                 ""Please install `interop-langchain` extra to use this module:

\tpip install ag2[interop-langchain]""
             )