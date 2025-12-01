@@ -6,7 +6,7 @@
 import pandas as pd
 from pydantic import BaseModel, Field
 
-from services.llm import request_to_chat_openai
+from services.llm import request_to_chat_ai
 
 
 class OverviewResponse(BaseModel):
@@ -36,7 +36,7 @@ def hierarchical_overview(config):
         input_text += descriptions[i] + ""

""
 
     messages = [{""role"": ""system"", ""content"": prompt}, {""role"": ""user"", ""content"": input_text}]
-    response = request_to_chat_openai(
+    response = request_to_chat_ai(
         messages=messages,
         model=model,
         provider=config[""provider""],