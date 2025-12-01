@@ -1,5 +1,5 @@
 import json
-from typing import Any, Dict, Optional
+from typing import Any
 
 from pydantic import BaseModel, Field
 
@@ -12,27 +12,28 @@ class CrewOutput(BaseModel):
     """"""Class that represents the result of a crew.""""""
 
     raw: str = Field(description=""Raw output of crew"", default="""")
-    pydantic: Optional[BaseModel] = Field(
-        description=""Pydantic output of Crew"", default=None
+    pydantic: BaseModel | None = Field(
+        description=""Pydantic output of Crew"", default=None,
     )
-    json_dict: Optional[Dict[str, Any]] = Field(
-        description=""JSON dict output of Crew"", default=None
+    json_dict: dict[str, Any] | None = Field(
+        description=""JSON dict output of Crew"", default=None,
     )
     tasks_output: list[TaskOutput] = Field(
-        description=""Output of each task"", default=[]
+        description=""Output of each task"", default=[],
     )
     token_usage: UsageMetrics = Field(description=""Processed token summary"", default={})
 
     @property
-    def json(self) -> Optional[str]:
+    def json(self) -> str | None:
         if self.tasks_output[-1].output_format != OutputFormat.JSON:
+            msg = ""No JSON output found in the final task. Please make sure to set the output_json property in the final task in your crew.""
             raise ValueError(
-                ""No JSON output found in the final task. Please make sure to set the output_json property in the final task in your crew.""
+                msg,
             )
 
         return json.dumps(self.json_dict)
 
-    def to_dict(self) -> Dict[str, Any]:
+    def to_dict(self) -> dict[str, Any]:
         """"""Convert json_output and pydantic_output to a dictionary.""""""
         output_dict = {}
         if self.json_dict:
@@ -44,12 +45,12 @@ def to_dict(self) -> Dict[str, Any]:
     def __getitem__(self, key):
         if self.pydantic and hasattr(self.pydantic, key):
             return getattr(self.pydantic, key)
-        elif self.json_dict and key in self.json_dict:
+        if self.json_dict and key in self.json_dict:
             return self.json_dict[key]
-        else:
-            raise KeyError(f""Key '{key}' not found in CrewOutput."")
+        msg = f""Key '{key}' not found in CrewOutput.""
+        raise KeyError(msg)
 
-    def __str__(self):
+    def __str__(self) -> str:
         if self.pydantic:
             return str(self.pydantic)
         if self.json_dict: