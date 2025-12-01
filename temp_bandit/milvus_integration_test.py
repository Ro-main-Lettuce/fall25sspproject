@@ -10,19 +10,21 @@
 import tempfile
 import time
 
-from airbyte_cdk.destinations.vector_db_based.embedder import OPEN_AI_VECTOR_SIZE
-from airbyte_cdk.destinations.vector_db_based.test_utils import BaseIntegrationTest
-from airbyte_cdk.models import DestinationSyncMode, Status
 from destination_milvus.destination import DestinationMilvus
 from langchain_community.embeddings import OpenAIEmbeddings
 from langchain_community.vectorstores import Milvus
 from pymilvus import Collection, CollectionSchema, DataType, FieldSchema, connections, utility
 
+from airbyte_cdk.destinations.vector_db_based.embedder import OPEN_AI_VECTOR_SIZE
+from airbyte_cdk.destinations.vector_db_based.test_utils import BaseIntegrationTest
+from airbyte_cdk.models import DestinationSyncMode, Status
+
+
 # Configure logging
 logger = logging.getLogger(""airbyte"")
 logger.setLevel(logging.DEBUG)
 handler = logging.StreamHandler(sys.stdout)
-handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
+handler.setFormatter(logging.Formatter(""%(asctime)s - %(name)s - %(levelname)s - %(message)s""))
 logger.addHandler(handler)
 
 
@@ -42,7 +44,7 @@ def _init_milvus(self):
         """"""Initialize Milvus Lite connection.""""""
         # Create the directory if it doesn't exist
         os.makedirs(self.temp_dir, exist_ok=True)
-        
+
         # Clean up existing connections - handle both string and tuple aliases
         for conn in connections.list_connections():
             alias = conn[0] if isinstance(conn, tuple) else conn
@@ -51,14 +53,14 @@ def _init_milvus(self):
                     connections.disconnect(alias)
             except Exception as e:
                 logger.warning(f""Failed to disconnect {alias}: {str(e)}"")
-        
+
         # Connect using Milvus Lite with a unique test alias
         try:
             connections.connect(
                 alias=""default"",  # Use same alias as indexer
                 uri=self.db_path,
                 use_lite=True,
-                timeout=30
+                timeout=30,
             )
             logger.info(f""Successfully connected to Milvus Lite at {self.db_path}"")
         except Exception as e:
@@ -71,37 +73,37 @@ def setUp(self):
         current_dir = os.path.dirname(os.path.abspath(__file__))
         secrets_path = os.path.join(current_dir, ""secrets"", ""config.json"")
         template_path = os.path.join(current_dir, ""config_template.json"")
-        
+
         config_path = secrets_path if os.path.exists(secrets_path) else template_path
         with open(config_path, ""r"") as f:
             self.config = json.loads(f.read())
-            
+
         # Create temporary directory for Milvus Lite
         self.temp_dir = tempfile.mkdtemp(prefix=""milvus_lite_"")
         self.db_path = os.path.join(self.temp_dir, ""milvus.db"")
-        
+
         # Override host configuration to use Milvus Lite
         self.config[""indexing""][""host""] = self.db_path
         self.config[""indexing""][""auth""] = {""mode"": ""no_auth""}
-        
+
         # Initialize Milvus Lite connection
         self._init_milvus()
 
     def tearDown(self):
         """"""Clean up Milvus Lite resources.""""""
         import shutil
-        
+
         try:
             # Clean up any existing test collections
-            if hasattr(self, 'config') and utility.has_collection(self.config[""indexing""][""collection""], using=""default""):
+            if hasattr(self, ""config"") and utility.has_collection(self.config[""indexing""][""collection""], using=""default""):
                 utility.drop_collection(self.config[""indexing""][""collection""], using=""default"")
-                
+
             # Disconnect from Milvus Lite
             if connections.has_connection(""default""):
                 connections.disconnect(""default"")
-            
+
             # Remove temporary directory
-            if hasattr(self, 'temp_dir'):
+            if hasattr(self, ""temp_dir""):
                 shutil.rmtree(self.temp_dir, ignore_errors=True)
         except Exception as e:
             logger.warning(f""Error during teardown: {str(e)}"")
@@ -118,10 +120,7 @@ def _create_collection(self, vector_dimensions=1536):
         schema = CollectionSchema(fields=[pk, vector], enable_dynamic_field=True)
         collection = Collection(name=self.config[""indexing""][""collection""], schema=schema, using=""default"")
         # Note: Milvus Lite only supports FLAT index type
-        collection.create_index(
-            field_name=""vector"",
-            index_params={""metric_type"": ""L2"", ""index_type"": ""FLAT""}
-        )
+        collection.create_index(field_name=""vector"", index_params={""metric_type"": ""L2"", ""index_type"": ""FLAT""})
 
     def test_check_valid_config_pre_created_collection(self):
         self._create_collection()
@@ -185,12 +184,16 @@ def test_write(self):
         class FakeEmbeddings:
             def embed_documents(self, texts):
                 return [[0.1] * OPEN_AI_VECTOR_SIZE for _ in texts]
-            
+
             def embed_query(self, text):
                 return [0.1] * OPEN_AI_VECTOR_SIZE
 
-        embeddings = FakeEmbeddings() if self.config[""embedding""][""mode""] == ""fake"" else OpenAIEmbeddings(openai_api_key=self.config[""embedding""][""openai_key""])
-        
+        embeddings = (
+            FakeEmbeddings()
+            if self.config[""embedding""][""mode""] == ""fake""
+            else OpenAIEmbeddings(openai_api_key=self.config[""embedding""][""openai_key""])
+        )
+
         # Skip LangChain integration test when using Milvus Lite
         # Note: LangChain's Milvus integration currently doesn't support Milvus Lite properly
         if not self.config[""indexing""][""host""].endswith("".db""):
@@ -205,7 +208,7 @@ def embed_query(self, text):
             vs.fields.append(""_ab_record_id"")
             results = vs.similarity_search(""Dogs"", k=1)
             assert len(results) == 1
-            
+
             # Additional similarity search test
             result = vs.similarity_search(""feline animals"", 1)
             assert len(result) == 1