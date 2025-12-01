@@ -37,15 +37,17 @@ def __init__(
         self._params = params
         self._stream = stream
 
-    T = TypeVar('T', str, List[str])
+    T = TypeVar(""T"", str, List[str])
 
     @overload
     def get(self, key: str) -> Optional[Union[str, List[str]]]: ...
 
     @overload
     def get(self, key: str, default: T) -> Union[str, List[str], T]: ...
 
-    def get(self, key: str, default: Optional[Union[str, List[str]]] = None) -> Optional[Union[str, List[str]]]:
+    def get(
+        self, key: str, default: Optional[Union[str, List[str]]] = None
+    ) -> Optional[Union[str, List[str]]]:
         """"""Get the value of the query parameter.
 
         Args:
@@ -167,15 +169,19 @@ def __init__(
     ):
         self._params = params
 
-    T = TypeVar('T', Primitive, List[Primitive])
+    T = TypeVar(""T"", Primitive, List[Primitive])
 
     @overload
     def get(self, key: str) -> Optional[ListOrValue[Primitive]]: ...
 
     @overload
-    def get(self, key: str, default: T) -> Union[ListOrValue[Primitive], T]: ...
+    def get(
+        self, key: str, default: T
+    ) -> Union[ListOrValue[Primitive], T]: ...
 
-    def get(self, key: str, default: Optional[ListOrValue[Primitive]] = None) -> Optional[ListOrValue[Primitive]]:
+    def get(
+        self, key: str, default: Optional[ListOrValue[Primitive]] = None
+    ) -> Optional[ListOrValue[Primitive]]:
         """"""Get the value of the CLI arg.
 
         Args: