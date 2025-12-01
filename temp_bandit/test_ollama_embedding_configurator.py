@@ -31,7 +31,7 @@ def test_ollama_respects_api_base_env_var(self):
                 model_name=""llama2""
             )
 
-    @patch.dict(os.environ, {""API_BASE"": ""http://env-ollama:8080""}, clear=True)
+    @patch.dict(os.environ, {""API_BASE"": ""http://env-ollama:8080/api/embeddings""}, clear=True)
     def test_ollama_config_url_overrides_env_var(self):
         config = {
             ""provider"": ""ollama"", 
@@ -84,7 +84,7 @@ def test_ollama_url_priority_order(self):
             )
 
     @patch.dict(os.environ, {""API_BASE"": ""http://localhost:11434/api/embeddings""}, clear=True)
-    def test_ollama_handles_full_url_in_api_base(self):
+    def test_ollama_uses_provided_url_as_is(self):
         config = {""provider"": ""ollama"", ""config"": {""model"": ""llama2""}}
         
         with patch(""chromadb.utils.embedding_functions.ollama_embedding_function.OllamaEmbeddingFunction"") as mock_ollama:
@@ -94,14 +94,15 @@ def test_ollama_handles_full_url_in_api_base(self):
                 model_name=""llama2""
             )
 
-    @patch.dict(os.environ, {""API_BASE"": ""http://localhost:11434/api/embeddings""}, clear=True)
-    def test_ollama_uses_provided_url_as_is(self):
+    @patch.dict(os.environ, {""API_BASE"": ""http://custom-base:9000""}, clear=True)
+    def test_ollama_requires_complete_url_in_api_base(self):
+        """"""Test that demonstrates users must provide complete URLs including endpoint.""""""
         config = {""provider"": ""ollama"", ""config"": {""model"": ""llama2""}}
         
         with patch(""chromadb.utils.embedding_functions.ollama_embedding_function.OllamaEmbeddingFunction"") as mock_ollama:
             self.configurator.configure_embedder(config)
             mock_ollama.assert_called_once_with(
-                url=""http://localhost:11434/api/embeddings"",
+                url=""http://custom-base:9000"",
                 model_name=""llama2""
             )
 