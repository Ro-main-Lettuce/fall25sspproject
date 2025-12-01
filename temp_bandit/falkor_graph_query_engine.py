@@ -4,18 +4,22 @@
 
 import os
 import warnings
+from typing import Optional
 
-from falkordb import FalkorDB, Graph
-from graphrag_sdk import KnowledgeGraph, Source
-from graphrag_sdk.model_config import KnowledgeGraphModelConfig
-from graphrag_sdk.models import GenerativeModel
-from graphrag_sdk.models.openai import OpenAiGenerativeModel
-from graphrag_sdk.ontology import Ontology
-
+from ....import_utils import optional_import_block, require_optional_import
 from .document import Document
 from .graph_query_engine import GraphStoreQueryResult
 
+with optional_import_block():
+    from falkordb import FalkorDB, Graph
+    from graphrag_sdk import KnowledgeGraph, Source
+    from graphrag_sdk.model_config import KnowledgeGraphModelConfig
+    from graphrag_sdk.models import GenerativeModel
+    from graphrag_sdk.models.openai import OpenAiGenerativeModel
+    from graphrag_sdk.ontology import Ontology
+
 
+@require_optional_import([""falkordb"", ""graphrag_sdk""], ""graph-rag-falkor-db"")
 class FalkorGraphQueryEngine:
     """"""This is a wrapper for FalkorDB KnowledgeGraph.""""""
 
@@ -24,10 +28,10 @@ def __init__(
         name: str,
         host: str = ""127.0.0.1"",
         port: int = 6379,
-        username: str | None = None,
-        password: str | None = None,
-        model: GenerativeModel = OpenAiGenerativeModel(""gpt-4o""),
-        ontology: Ontology | None = None,
+        username: Optional[str] = None,
+        password: Optional[str] = None,
+        model: Optional[""GenerativeModel""] = None,
+        ontology: Optional[""Ontology""] = None,
     ):
         """"""Initialize a FalkorDB knowledge graph.
         Please also refer to https://github.com/FalkorDB/GraphRAG-SDK/blob/main/graphrag_sdk/kg.py
@@ -50,7 +54,7 @@ def __init__(
         self.port = port
         self.username = username
         self.password = password
-        self.model = model
+        self.model = model or OpenAiGenerativeModel(""gpt-4o"")
         self.model_config = KnowledgeGraphModelConfig.with_model(model)
         self.ontology = ontology
         self.knowledge_graph = None
@@ -149,17 +153,17 @@ def delete(self) -> bool:
             self.falkordb.select_graph(self.ontology_table_name).delete()
         return True
 
-    def __get_ontology_storage_graph(self) -> Graph:
+    def __get_ontology_storage_graph(self) -> ""Graph"":
         return self.falkordb.select_graph(self.ontology_table_name)
 
-    def _save_ontology_to_db(self, ontology: Ontology):
+    def _save_ontology_to_db(self, ontology: ""Ontology""):
         """"""Save graph ontology to a separate table with {graph_name}_ontology""""""
         if self.ontology_table_name in self.falkordb.list_graphs():
             raise ValueError(f""Knowledge graph {self.name} is already created."")
         graph = self.__get_ontology_storage_graph()
         ontology.save_to_graph(graph)
 
-    def _load_ontology_from_db(self) -> Ontology:
+    def _load_ontology_from_db(self) -> ""Ontology"":
         if self.ontology_table_name not in self.falkordb.list_graphs():
             raise ValueError(f""Knowledge graph {self.name} has not been created."")
         graph = self.__get_ontology_storage_graph()