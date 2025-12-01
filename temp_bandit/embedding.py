@@ -1,3 +1,5 @@
+import os
+
 import pandas as pd
 from tqdm import tqdm
 
@@ -23,7 +25,7 @@ def embedding(config):
             is_embedded_at_local,
             config[""provider""],
             local_llm_address=config.get(""local_llm_address""),
-            user_api_key=config.get(""user_api_key""),
+            user_api_key=os.getenv(""USER_API_KEY""),
         )
         embeddings.extend(embeds)
     df = pd.DataFrame([{""arg-id"": arguments.iloc[i][""arg-id""], ""embedding"": e} for i, e in enumerate(embeddings)])