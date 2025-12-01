@@ -8,7 +8,7 @@
 from tqdm import tqdm
 
 from services.category_classification import classify_args
-from services.llm import request_to_chat_openai
+from services.llm import request_to_chat_ai
 from services.parse_json_list import parse_extraction_response
 from utils import update_progress
 
@@ -128,7 +128,7 @@ def extract_arguments(input, prompt, model, provider=""openai"", local_llm_address
         {""role"": ""user"", ""content"": input},
     ]
     try:
-        response = request_to_chat_openai(
+        response = request_to_chat_ai(
             messages=messages,
             model=model,
             is_json=False,