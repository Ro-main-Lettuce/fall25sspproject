@@ -33,15 +33,19 @@ class MockStdout(Stdout):
         def __init__(self) -> None:
             self.written_data: list[tuple[str, KnownMimeType]] = []
 
-        def _write_with_mimetype(self, data: str, mimetype: KnownMimeType) -> int:
+        def _write_with_mimetype(
+            self, data: str, mimetype: KnownMimeType
+        ) -> int:
             self.written_data.append((data, mimetype))
             return len(data)
 
     class MockStderr(Stderr):
         def __init__(self) -> None:
             self.written_data: list[tuple[str, KnownMimeType]] = []
 
-        def _write_with_mimetype(self, data: str, mimetype: KnownMimeType) -> int:
+        def _write_with_mimetype(
+            self, data: str, mimetype: KnownMimeType
+        ) -> int:
             self.written_data.append((data, mimetype))
             return len(data)
 