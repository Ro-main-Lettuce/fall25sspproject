@@ -2,26 +2,35 @@
 #
 # SPDX-License-Identifier: Apache-2.0
 import os
-from typing import Optional, TypeAlias, Union
-
-from llama_index.core import PropertyGraphIndex, SimpleDirectoryReader
-from llama_index.core.base.embeddings.base import BaseEmbedding
-from llama_index.core.indices.property_graph import (
-    DynamicLLMPathExtractor,
-    SchemaLLMPathExtractor,
-)
-from llama_index.core.indices.property_graph.transformations.schema_llm import Triple
-from llama_index.core.llms import LLM
-from llama_index.core.readers.json import JSONReader
-from llama_index.core.schema import Document as LlamaDocument
-from llama_index.embeddings.openai import OpenAIEmbedding
-from llama_index.graph_stores.neo4j import Neo4jPropertyGraphStore
-from llama_index.llms.openai import OpenAI
+import sys
+from typing import Optional, Union
 
+if sys.version_info >= (3, 10):
+    from typing import TypeAlias
+else:
+    from typing_extensions import TypeAlias
+
+from ....import_utils import optional_import_block, require_optional_import
 from .document import Document, DocumentType
 from .graph_query_engine import GraphQueryEngine, GraphStoreQueryResult
 
-
+with optional_import_block():
+    from llama_index.core import PropertyGraphIndex, SimpleDirectoryReader
+    from llama_index.core.base.embeddings.base import BaseEmbedding
+    from llama_index.core.indices.property_graph import (
+        DynamicLLMPathExtractor,
+        SchemaLLMPathExtractor,
+    )
+    from llama_index.core.indices.property_graph.transformations.schema_llm import Triple
+    from llama_index.core.llms import LLM
+    from llama_index.core.readers.json import JSONReader
+    from llama_index.core.schema import Document as LlamaDocument
+    from llama_index.embeddings.openai import OpenAIEmbedding
+    from llama_index.graph_stores.neo4j import Neo4jPropertyGraphStore
+    from llama_index.llms.openai import OpenAI
+
+
+@require_optional_import(""llama_index"", ""neo4j"")
 class Neo4jGraphQueryEngine(GraphQueryEngine):
     """"""This class serves as a wrapper for a property graph query engine backed by LlamaIndex and Neo4j,
     facilitating the creating, connecting, updating, and querying of LlamaIndex property graphs.
@@ -49,11 +58,11 @@ def __init__(
         database: str = ""neo4j"",
         username: str = ""neo4j"",
         password: str = ""neo4j"",
-        llm: LLM = OpenAI(model=""gpt-4o"", temperature=0.0),
-        embedding: BaseEmbedding = OpenAIEmbedding(model_name=""text-embedding-3-small""),
-        entities: Optional[TypeAlias] = None,
-        relations: Optional[TypeAlias] = None,
-        schema: Optional[Union[dict[str, str], list[Triple]]] = None,
+        llm: Optional[""LLM""] = None,
+        embedding: Optional[""BaseEmbedding""] = None,
+        entities: Optional[""TypeAlias""] = None,
+        relations: Optional[""TypeAlias""] = None,
+        schema: Optional[Union[dict[str, str], list[""Triple""]]] = None,
         strict: Optional[bool] = False,
     ):
         """"""Initialize a Neo4j Property graph.
@@ -78,14 +87,14 @@ def __init__(
         self.database = database
         self.username = username
         self.password = password
-        self.llm = llm
-        self.embedding = embedding
+        self.llm = llm or OpenAI(model=""gpt-4o"", temperature=0.0)
+        self.embedding = embedding or OpenAIEmbedding(model_name=""text-embedding-3-small"")
         self.entities = entities
         self.relations = relations
         self.schema = schema
         self.strict = strict
 
-    def init_db(self, input_doc: list[Document] | None = None):
+    def init_db(self, input_doc: Optional[list[Document]] = None):
         """"""Build the knowledge graph with input documents.""""""
         self.documents = self._load_doc(input_doc)
 
@@ -188,7 +197,7 @@ def _clear(self) -> None:
         with self.graph_store._driver.session() as session:
             session.run(""MATCH (n) DETACH DELETE n;"")
 
-    def _load_doc(self, input_doc: list[Document]) -> list[LlamaDocument]:
+    def _load_doc(self, input_doc: list[Document]) -> list[""LlamaDocument""]:
         """"""Load documents from the input files. Currently support the following file types:
         .csv - comma-separated values
         .docx - Microsoft Word