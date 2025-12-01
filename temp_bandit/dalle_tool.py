@@ -1,11 +1,10 @@
 import json
 from typing import Type
 
+from crewai.tools import BaseTool
 from openai import OpenAI
 from pydantic import BaseModel
 
-from crewai_tools.tools.base_tool import BaseTool
-
 
 class ImagePromptSchema(BaseModel):
     """"""Input for Dall-E Tool.""""""