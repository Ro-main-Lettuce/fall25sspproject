@@ -14,11 +14,17 @@
 
 class FrameworkImporter(MetaPathFinder):
     def find_spec(
-        self, fullname: str, path: Sequence[str] | None, target: ModuleType | None = ...
+        self,
+        fullname: str,
+        path: Sequence[str] | None,
+        target: ModuleType | None = None,
     ) -> ModuleSpec | None:
-        if not fullname.startswith(""bentoml.""):
+        if not fullname.startswith(""bentoml."") or fullname.startswith(""bentoml._""):
             return None
-        framework = fullname.split(""."")[1]
+        parts = fullname.split(""."")
+        if len(parts) < 2:
+            return None
+        framework = parts[1]
         if ""."" in framework:
             return None
         spec = importlib.util.find_spec(f""_bentoml_impl.frameworks.{framework}"")