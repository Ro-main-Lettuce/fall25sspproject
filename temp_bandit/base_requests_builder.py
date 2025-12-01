@@ -34,13 +34,12 @@ def build(self) -> HttpRequest:
 
 
 class MondayBaseRequestBuilder(MondayRequestBuilder):
-    def __init__(self, resource: str = """") -> None:
-        self._resource: str = resource
+    def __init__(self) -> None:
         self._authenticator: str = None
 
     @property
     def url(self) -> str:
-        return f""https://api.monday.com/v2/{self._resource}""
+        return f""https://api.monday.com/v2""
 
     @property
     def headers(self) -> Dict[str, Any]: