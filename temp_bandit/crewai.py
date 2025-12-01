@@ -6,6 +6,7 @@
 import sys
 from typing import Any, Optional
 
+from ...import_utils import optional_import_block
 from ...tools import Tool
 from ..registry import register_interoperable_class
 
@@ -73,9 +74,10 @@ def get_unsupported_reason(cls) -> Optional[str]:
         if sys.version_info < (3, 10) or sys.version_info >= (3, 13):
             return ""This submodule is only supported for Python versions 3.10, 3.11, and 3.12""
 
-        try:
+        with optional_import_block() as result:
             import crewai.tools  # noqa: F401
-        except ImportError:
+
+        if not result.is_successful:
             return ""Please install `interop-crewai` extra to use this module:

\tpip install ag2[interop-crewai]""
 
         return None