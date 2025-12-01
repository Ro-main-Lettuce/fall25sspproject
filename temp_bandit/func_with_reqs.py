@@ -4,7 +4,6 @@
 #
 # Portions derived from https://github.com/microsoft/autogen are under the MIT License.
 # SPDX-License-Identifier: MIT
-from __future__ import annotations
 
 import functools
 import importlib
@@ -20,7 +19,7 @@
 P = ParamSpec(""P"")
 
 
-def _to_code(func: FunctionWithRequirements[T, P] | Callable[P, T] | FunctionWithRequirementsStr) -> str:
+def _to_code(func: Union[""FunctionWithRequirements[T, P]"", Callable[P, T], ""FunctionWithRequirementsStr""]) -> str:
     if isinstance(func, FunctionWithRequirementsStr):
         return func.func
 
@@ -40,7 +39,7 @@ class Alias:
 @dataclass
 class ImportFromModule:
     module: str
-    imports: list[str | Alias]
+    imports: list[Union[str, Alias]]
 
 
 Import = Union[str, ImportFromModule, Alias]
@@ -53,7 +52,7 @@ def _import_to_str(im: Import) -> str:
         return f""import {im.name} as {im.alias}""
     else:
 
-        def to_str(i: str | Alias) -> str:
+        def to_str(i: Union[str, Alias]) -> str:
             if isinstance(i, str):
                 return i
             else:
@@ -123,7 +122,7 @@ class FunctionWithRequirements(Generic[T, P]):
     @classmethod
     def from_callable(
         cls, func: Callable[P, T], python_packages: list[str] = [], global_imports: list[Import] = []
-    ) -> FunctionWithRequirements[T, P]:
+    ) -> ""FunctionWithRequirements[T, P]"":
         return cls(python_packages=python_packages, global_imports=global_imports, func=func)
 
     @staticmethod
@@ -162,7 +161,7 @@ def wrapper(func: Callable[P, T]) -> FunctionWithRequirements[T, P]:
 
 
 def _build_python_functions_file(
-    funcs: list[FunctionWithRequirements[Any, P] | Callable[..., Any] | FunctionWithRequirementsStr],
+    funcs: list[Union[FunctionWithRequirements[Any, P], Callable[..., Any], FunctionWithRequirementsStr]],
 ) -> str:
     # First collect all global imports
     global_imports: set[str] = set()
@@ -178,7 +177,7 @@ def _build_python_functions_file(
     return content
 
 
-def to_stub(func: Callable[..., Any] | FunctionWithRequirementsStr) -> str:
+def to_stub(func: Union[Callable[..., Any], FunctionWithRequirementsStr]) -> str:
     """"""Generate a stub for a function as a string
 
     Args: