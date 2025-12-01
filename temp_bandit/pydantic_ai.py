@@ -9,6 +9,7 @@
 from inspect import signature
 from typing import Any, Callable, Optional
 
+from ...import_utils import optional_import_block
 from ..registry import register_interoperable_class
 from .pydantic_ai_tool import PydanticAITool as AG2PydanticAITool
 
@@ -151,9 +152,10 @@ def get_unsupported_reason(cls) -> Optional[str]:
         if sys.version_info < (3, 9):
             return ""This submodule is only supported for Python versions 3.9 and above""
 
-        try:
+        with optional_import_block() as result:
             import pydantic_ai.tools  # noqa: F401
-        except ImportError:
+
+        if not result.is_successful:
             return ""Please install `interop-pydantic-ai` extra to use this module:

\tpip install ag2[interop-pydantic-ai]""
 
         return None