@@ -1,9 +1,8 @@
 from typing import Type
 
+from crewai.tools import BaseTool
 from pydantic import BaseModel, Field
 
-from crewai_tools.tools.base_tool import BaseTool
-
 
 class EXABaseToolToolSchema(BaseModel):
     """"""Input for EXABaseTool.""""""
@@ -27,10 +26,10 @@ class EXABaseTool(BaseTool):
     }
 
     def _parse_results(self, results):
-        stirng = []
+        string = []
         for result in results:
             try:
-                stirng.append(
+                string.append(
                     ""
"".join(
                         [
                             f""Title: {result['title']}"",
@@ -42,7 +41,7 @@ def _parse_results(self, results):
                     )
                 )
             except KeyError:
-                next
+                continue
 
-        content = ""
"".join(stirng)
+        content = ""
"".join(string)
         return f""
Search results: {content}
""