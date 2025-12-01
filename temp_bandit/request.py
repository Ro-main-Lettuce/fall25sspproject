@@ -9,6 +9,7 @@
 from typing import Any, Generic
 from pydantic import BaseModel, Field
 import json
+import io
 from .models import T
 
 
@@ -151,14 +152,25 @@ def to_anthropic_format(self) -> dict[str, Any]:
             ""params"": params,
         }
 
-    def save_to_file(self, file_path: str, provider: str) -> None:
-        """"""Save batch request to file in provider-specific format""""""
+    def save_to_file(
+        self, file_path_or_buffer: str | io.BytesIO, provider: str
+    ) -> None:
+        """"""Save batch request to file or BytesIO buffer in provider-specific format""""""
         if provider == ""openai"":
             data = self.to_openai_format()
         elif provider == ""anthropic"":
             data = self.to_anthropic_format()
         else:
             raise ValueError(f""Unsupported provider: {provider}"")
 
-        with open(file_path, ""a"") as f:
-            f.write(json.dumps(data) + ""
"")
+        json_line = json.dumps(data) + ""
""
+
+        if isinstance(file_path_or_buffer, str):
+            with open(file_path_or_buffer, ""a"") as f:
+                f.write(json_line)
+        elif isinstance(file_path_or_buffer, io.BytesIO):
+            file_path_or_buffer.write(json_line.encode(""utf-8""))
+        else:
+            raise ValueError(
+                f""Unsupported file_path_or_buffer type: {type(file_path_or_buffer)}""
+            )