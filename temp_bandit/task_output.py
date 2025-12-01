@@ -1,5 +1,5 @@
 import json
-from typing import Any, Dict, Optional
+from typing import Any
 
 from pydantic import BaseModel, Field, model_validator
 
@@ -10,21 +10,21 @@ class TaskOutput(BaseModel):
     """"""Class that represents the result of a task.""""""
 
     description: str = Field(description=""Description of the task"")
-    name: Optional[str] = Field(description=""Name of the task"", default=None)
-    expected_output: Optional[str] = Field(
-        description=""Expected output of the task"", default=None
+    name: str | None = Field(description=""Name of the task"", default=None)
+    expected_output: str | None = Field(
+        description=""Expected output of the task"", default=None,
     )
-    summary: Optional[str] = Field(description=""Summary of the task"", default=None)
+    summary: str | None = Field(description=""Summary of the task"", default=None)
     raw: str = Field(description=""Raw output of the task"", default="""")
-    pydantic: Optional[BaseModel] = Field(
-        description=""Pydantic output of task"", default=None
+    pydantic: BaseModel | None = Field(
+        description=""Pydantic output of task"", default=None,
     )
-    json_dict: Optional[Dict[str, Any]] = Field(
-        description=""JSON dictionary of task"", default=None
+    json_dict: dict[str, Any] | None = Field(
+        description=""JSON dictionary of task"", default=None,
     )
     agent: str = Field(description=""Agent that executed the task"")
     output_format: OutputFormat = Field(
-        description=""Output format of the task"", default=OutputFormat.RAW
+        description=""Output format of the task"", default=OutputFormat.RAW,
     )
 
     @model_validator(mode=""after"")
@@ -35,19 +35,22 @@ def set_summary(self):
         return self
 
     @property
-    def json(self) -> Optional[str]:
+    def json(self) -> str | None:
         if self.output_format != OutputFormat.JSON:
-            raise ValueError(
+            msg = (
                 """"""
                 Invalid output format requested.
                 If you would like to access the JSON output,
                 please make sure to set the output_json property for the task
                 """"""
             )
+            raise ValueError(
+                msg,
+            )
 
         return json.dumps(self.json_dict)
 
-    def to_dict(self) -> Dict[str, Any]:
+    def to_dict(self) -> dict[str, Any]:
         """"""Convert json_output and pydantic_output to a dictionary.""""""
         output_dict = {}
         if self.json_dict: