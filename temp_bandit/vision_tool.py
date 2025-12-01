@@ -2,11 +2,10 @@
 from typing import Type
 
 import requests
+from crewai.tools import BaseTool
 from openai import OpenAI
 from pydantic import BaseModel
 
-from crewai_tools.tools.base_tool import BaseTool
-
 
 class ImagePromptSchema(BaseModel):
     """"""Input for Vision Tool.""""""