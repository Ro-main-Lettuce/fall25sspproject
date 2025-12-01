@@ -8,7 +8,7 @@
 from pydantic import BaseModel, Field
 from tqdm import tqdm
 
-from services.llm import request_to_chat_openai
+from services.llm import request_to_chat_ai
 
 
 @dataclass
@@ -270,7 +270,7 @@ def filter_previous_values(df: pd.DataFrame, previous_columns: ClusterColumns) -
         },
     ]
     try:
-        response = request_to_chat_openai(
+        response = request_to_chat_ai(
             messages=messages,
             model=config[""hierarchical_merge_labelling""][""model""],
             json_schema=LabellingFromat,