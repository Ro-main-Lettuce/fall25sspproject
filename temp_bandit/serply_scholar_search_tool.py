@@ -3,10 +3,9 @@
 from urllib.parse import urlencode
 
 import requests
+from crewai.tools import BaseTool
 from pydantic import BaseModel, Field
 
-from crewai_tools.tools.base_tool import BaseTool
-
 
 class SerplyScholarSearchToolSchema(BaseModel):
     """"""Input for Serply Scholar Search.""""""