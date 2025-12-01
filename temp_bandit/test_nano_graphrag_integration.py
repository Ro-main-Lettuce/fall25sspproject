@@ -44,8 +44,8 @@ def test_nano_graphrag_integration():
         
         ollama_client = OllamaClient()
         ollama_config = {
-            ""generation_model"": ""qwen2.5:0.5b"",
-            ""embedding_model"": ""nomic-embed-text"",
+            ""generation_model"": ""qwen2.5:0.5b"",  # Can be any model user has configured
+            ""embedding_model"": ""nomic-embed-text"",  # Can be any embedding model user has configured
             ""embedding_dim"": 768
         }
         