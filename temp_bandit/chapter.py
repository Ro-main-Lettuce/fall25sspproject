@@ -37,7 +37,7 @@ def __repr__(self):
 
 
 def load_chapters_from_api(doc_id, base_url=cfg.API_URL) -> tuple[list[Chapter], str]:
-    url = f""{base_url}/lesson/get_chatper_info""
+    url = f""{base_url}/lesson/get_chapter_info""
     params = {""doc_id"": doc_id}
 
     response = requests.get(url, params=params)