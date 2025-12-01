@@ -108,17 +108,19 @@ def _validate_url(url):
         except ValueError:
             return False
 
-    @staticmethod
-    def _construct_embeddings_url(base_url):
-        """"""Construct the full embeddings URL from a base URL.""""""
-        if not base_url:
-            return ""http://localhost:11434/api/embeddings""
-        
-        base_url = base_url.rstrip('/')
-        return f""{base_url}/api/embeddings"" if not base_url.endswith('/api/embeddings') else base_url
-
     @staticmethod
     def _configure_ollama(config, model_name):
+        """"""Configure Ollama embedding function.
+        
+        Supports configuration via:
+        1. config.url - Direct URL to Ollama embeddings endpoint
+        2. config.api_base - Base URL for Ollama API 
+        3. API_BASE environment variable - Base URL from environment
+        4. Default: http://localhost:11434/api/embeddings
+        
+        Note: When using api_base or API_BASE, ensure the URL includes the full
+        embeddings endpoint path (e.g., http://localhost:11434/api/embeddings)
+        """"""
         from chromadb.utils.embedding_functions.ollama_embedding_function import (
             OllamaEmbeddingFunction,
         )
@@ -127,12 +129,11 @@ def _configure_ollama(config, model_name):
             config.get(""url"") 
             or config.get(""api_base"") 
             or os.getenv(""API_BASE"")
+            or ""http://localhost:11434/api/embeddings""
         )
         
-        if url and not EmbeddingConfigurator._validate_url(url):
+        if not EmbeddingConfigurator._validate_url(url):
             raise ValueError(f""Invalid Ollama API URL: {url}"")
-        
-        url = EmbeddingConfigurator._construct_embeddings_url(url)
 
         return OllamaEmbeddingFunction(
             url=url,