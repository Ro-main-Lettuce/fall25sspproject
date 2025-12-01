@@ -7,11 +7,14 @@
 from __future__ import annotations
 
 from collections.abc import Iterable
-from typing import Literal
+from typing import Literal, Optional
 
-try:
+from .import_utils import optional_import_block
+
+with optional_import_block() as result:
     from termcolor import colored
-except ImportError:
+
+if not result.is_successful:
     # termcolor is an optional dependency - if it cannot be imported then no color is used.
     # Alternatively the envvar NO_COLOR can be used to disable color.
     # To allow for proper typing and for termcolor to be optional we need to re-define the types used in the lib here.
@@ -67,12 +70,12 @@
 
     def colored(
         text: object,
-        color: Color | None = None,
-        on_color: Highlight | None = None,
-        attrs: Iterable[Attribute] | None = None,
+        color: Optional[Color] = None,
+        on_color: Optional[Highlight] = None,
+        attrs: Optional[Iterable[Attribute]] = None,
         *,
-        no_color: bool | None = None,
-        force_color: bool | None = None,
+        no_color: Optional[bool] = None,
+        force_color: Optional[bool] = None,
     ) -> str:
         return str(text)
 