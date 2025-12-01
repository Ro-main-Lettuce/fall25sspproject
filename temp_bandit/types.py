@@ -14,7 +14,8 @@ class VizNode:
     file_path: str | None = None
     symbol_name: str | None = None
 
+
 @dataclass(frozen=True)
 class GraphJson:
     type: str
-    data: dict
\ No newline at end of file
+    data: dict