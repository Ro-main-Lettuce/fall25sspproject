@@ -1,10 +1,9 @@
 import os
 from typing import Any, Optional, Type
 
+from crewai.tools import BaseTool
 from pydantic import BaseModel, Field
 
-from ..base_tool import BaseTool
-
 
 class FixedDirectoryReadToolSchema(BaseModel):
     """"""Input for DirectoryReadTool.""""""