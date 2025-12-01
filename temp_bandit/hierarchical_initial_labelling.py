@@ -6,7 +6,7 @@
 import pandas as pd
 from pydantic import BaseModel, Field
 
-from services.llm import request_to_chat_openai
+from services.llm import request_to_chat_ai
 
 
 class LabellingResult(TypedDict):
@@ -144,7 +144,7 @@ def process_initial_labelling(
         {""role"": ""user"", ""content"": input},
     ]
     try:
-        response = request_to_chat_openai(
+        response = request_to_chat_ai(
             messages=messages,
             model=model,
             provider=provider,