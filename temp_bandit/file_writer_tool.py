@@ -1,16 +1,16 @@
 import os
+from distutils.util import strtobool
 from typing import Any, Optional, Type
 
+from crewai.tools import BaseTool
 from pydantic import BaseModel
 
-from ..base_tool import BaseTool
-
 
 class FileWriterToolInput(BaseModel):
     filename: str
+    directory: Optional[str] = ""./""
+    overwrite: str = ""False""
     content: str
-    directory: Optional[str] = None
-    overwrite: bool = False
 
 
 class FileWriterTool(BaseTool):
@@ -21,11 +21,14 @@ class FileWriterTool(BaseTool):
     def _run(self, **kwargs: Any) -> str:
         try:
             # Create the directory if it doesn't exist
-            if kwargs[""directory""] and not os.path.exists(kwargs[""directory""]):
+            if kwargs.get(""directory"") and not os.path.exists(kwargs[""directory""]):
                 os.makedirs(kwargs[""directory""])
 
             # Construct the full path
-            filepath = os.path.join(kwargs[""directory""] or """", kwargs[""filename""])
+            filepath = os.path.join(kwargs.get(""directory"") or """", kwargs[""filename""])
+
+            # Convert overwrite to boolean
+            kwargs[""overwrite""] = bool(strtobool(kwargs[""overwrite""]))
 
             # Check if file exists and overwrite is not allowed
             if os.path.exists(filepath) and not kwargs[""overwrite""]:
@@ -40,5 +43,7 @@ def _run(self, **kwargs: Any) -> str:
             return (
                 f""File {filepath} already exists and overwrite option was not passed.""
             )
+        except KeyError as e:
+            return f""An error occurred while accessing key: {str(e)}""
         except Exception as e:
             return f""An error occurred while writing to the file: {str(e)}""