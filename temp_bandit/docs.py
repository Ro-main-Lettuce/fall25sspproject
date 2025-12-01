@@ -1,10 +1,9 @@
-from codegen.shared.decorators.types import DocumentedObject
 import bisect
 import inspect
 from collections.abc import Callable
-from dataclasses import dataclass
 from typing import TypeVar
 
+from codegen.shared.decorators.types import DocumentedObject
 
 apidoc_objects: list[DocumentedObject] = []
 