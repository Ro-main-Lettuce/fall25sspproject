@@ -1,11 +1,10 @@
 import json
 from typing import Optional, Type
 
+from crewai.tools import BaseTool
 from e2b_code_interpreter import Sandbox
 from pydantic import BaseModel, Field
 
-from ..base_tool import BaseTool
-
 
 class E2BCodeInterpreterSchema(BaseModel):
     """"""Input schema for the CodeInterpreterTool, used by the agent.""""""