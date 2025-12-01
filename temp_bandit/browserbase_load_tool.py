@@ -1,9 +1,8 @@
 from typing import Any, Optional, Type
 
+from crewai.tools import BaseTool
 from pydantic import BaseModel, Field
 
-from crewai_tools.tools.base_tool import BaseTool
-
 
 class BrowserbaseLoadToolSchema(BaseModel):
     url: str = Field(description=""Website URL"")