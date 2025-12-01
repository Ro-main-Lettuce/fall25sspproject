@@ -18,7 +18,7 @@ class OverviewBuilder:
         ""DOCUMENT_START:
{text}

OVERVIEW:""
     )
 
-    def __init__(self, llm_client, model: str = ""qwen3:0.6b"", first_n_chunks: int = 5,
+    def __init__(self, llm_client, model: str = ""llama3.2:latest"", first_n_chunks: int = 5,
                  out_path: str | None = None):
         if out_path is None:
             out_path = ""index_store/overviews/overviews.jsonl""
@@ -44,4 +44,4 @@ def build_and_store(self, doc_id: str, chunks: List[Dict[str, Any]]):
         with open(self.out_path, ""a"", encoding=""utf-8"") as f:
             f.write(json.dumps(record, ensure_ascii=False) + ""
"")
 
-        logger.info(f""📄 Overview generated for {doc_id} (stored in {self.out_path})"") 
\ No newline at end of file
+        logger.info(f""📄 Overview generated for {doc_id} (stored in {self.out_path})"")  
\ No newline at end of file