@@ -12,7 +12,7 @@
 from typing import Literal
 
 import pandas as pd
-from broadlistening.pipeline.services.llm import request_to_chat_openai
+from broadlistening.pipeline.services.llm import request_to_chat_ai
 
 
 def get_criteria_clarity() -> str:
@@ -222,7 +222,7 @@ def evaluate_batch_clarity_coherence_distinctiveness(cluster_data: dict, model:
         {""role"": ""user"", ""content"": format_batch_prompt_for_ccd(cluster_data)}
     ]
     try:
-        response = request_to_chat_openai(messages=messages, model=model, is_json=True)
+        response = request_to_chat_ai(messages=messages, model=model, is_json=True)
         results = json.loads(response)
         for cluster_id in cluster_data:
             if cluster_id in results:
@@ -243,7 +243,7 @@ def evaluate_consistency_per_cluster(cluster_data: dict, model: str) -> dict:
             {""role"": ""user"", ""content"": prompt}
         ]
         try:
-            response = request_to_chat_openai(messages=messages, model=model, is_json=True)
+            response = request_to_chat_ai(messages=messages, model=model, is_json=True)
             result = json.loads(response)
             results[cluster_id] = result
         except Exception as e: