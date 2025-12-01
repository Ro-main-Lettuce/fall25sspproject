@@ -6,23 +6,26 @@
 import logging
 from typing import List, Optional, Union
 
-from neo4j import GraphDatabase
-from neo4j_graphrag.embeddings import Embedder, OpenAIEmbeddings
-from neo4j_graphrag.experimental.pipeline.kg_builder import SimpleKGPipeline
-from neo4j_graphrag.generation import GraphRAG
-from neo4j_graphrag.indexes import create_vector_index
-from neo4j_graphrag.llm.openai_llm import LLMInterface, OpenAILLM
-from neo4j_graphrag.retrievers import VectorRetriever
-
+from ....import_utils import optional_import_block, require_optional_import
 from .document import Document, DocumentType
 from .graph_query_engine import GraphQueryEngine, GraphStoreQueryResult
 
+with optional_import_block():
+    from neo4j import GraphDatabase
+    from neo4j_graphrag.embeddings import Embedder, OpenAIEmbeddings
+    from neo4j_graphrag.experimental.pipeline.kg_builder import SimpleKGPipeline
+    from neo4j_graphrag.generation import GraphRAG
+    from neo4j_graphrag.indexes import create_vector_index
+    from neo4j_graphrag.llm.openai_llm import LLMInterface, OpenAILLM
+    from neo4j_graphrag.retrievers import VectorRetriever
+
 # Set up logging
 logging.basicConfig(level=logging.INFO)
 logging.getLogger(""httpx"").setLevel(logging.WARNING)
 logger = logging.getLogger(__name__)
 
 
+@require_optional_import([""neo4j"", ""neo4j_graphrag""], ""neo4j"")
 class Neo4jNativeGraphQueryEngine(GraphQueryEngine):
     """"""A graph query engine implemented using the Neo4j GraphRAG SDK.
     Provides functionality to initialize a knowledge graph,
@@ -35,13 +38,10 @@ def __init__(
         port: int = 7687,
         username: str = ""neo4j"",
         password: str = ""password"",
-        embeddings: Optional[Embedder] = OpenAIEmbeddings(model=""text-embedding-3-large""),
+        embeddings: Optional[""Embedder""] = None,
         embedding_dimension: Optional[int] = 3072,
-        llm: Optional[LLMInterface] = OpenAILLM(
-            model_name=""gpt-4o"",
-            model_params={""response_format"": {""type"": ""json_object""}, ""temperature"": 0},
-        ),
-        query_llm: Optional[LLMInterface] = OpenAILLM(model_name=""gpt-4o"", model_params={""temperature"": 0}),
+        llm: Optional[""LLMInterface""] = None,
+        query_llm: Optional[""LLMInterface""] = None,
         entities: Optional[List[str]] = None,
         relations: Optional[List[str]] = None,
         potential_schema: Optional[List[tuple[str, str, str]]] = None,
@@ -64,10 +64,13 @@ def __init__(
         """"""
         self.uri = f""{host}:{port}""
         self.driver = GraphDatabase.driver(self.uri, auth=(username, password))
-        self.embeddings = embeddings
+        self.embeddings = embeddings or OpenAIEmbeddings(model=""text-embedding-3-large"")
         self.embedding_dimension = embedding_dimension
-        self.llm = llm
-        self.query_llm = query_llm
+        self.llm = llm or OpenAILLM(
+            model_name=""gpt-4o"",
+            model_params={""response_format"": {""type"": ""json_object""}, ""temperature"": 0},
+        )
+        self.query_llm = query_llm or OpenAILLM(model_name=""gpt-4o"", model_params={""temperature"": 0})
         self.entities = entities
         self.relations = relations
         self.potential_schema = potential_schema