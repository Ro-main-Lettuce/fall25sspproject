@@ -4,7 +4,7 @@
 import os
 import shutil
 import uuid
-from typing import Any, Dict, List, Optional, Union
+from typing import Any, Dict, List, Optional
 
 try:
     from chromadb.api import ClientAPI
@@ -16,6 +16,7 @@
 from crewai.memory.storage.base_rag_storage import BaseRAGStorage
 from crewai.utilities import EmbeddingConfigurator
 from crewai.utilities.constants import MAX_FILE_NAME_LENGTH
+from crewai.utilities.errors import ChromaDBRequiredError
 from crewai.utilities.paths import db_storage_path
 
 
@@ -66,10 +67,7 @@ def _set_embedder_config(self):
 
     def _initialize_app(self):
         if not HAS_CHROMADB:
-            raise ImportError(
-                ""ChromaDB is required for memory storage features. ""
-                ""Please install it with 'pip install crewai[storage]'""
-            )
+            raise ChromaDBRequiredError(""memory storage"")
             
         try:
             import chromadb
@@ -92,10 +90,7 @@ def _initialize_app(self):
                     name=self.type, embedding_function=self.embedder_config
                 )
         except ImportError:
-            raise ImportError(
-                ""ChromaDB is required for memory storage features. ""
-                ""Please install it with 'pip install crewai[storage]'""
-            )
+            raise ChromaDBRequiredError(""memory storage"")
 
     def _sanitize_role(self, role: str) -> str:
         """"""
@@ -183,10 +178,7 @@ def reset(self) -> None:
 
     def _create_default_embedding_function(self):
         if not HAS_CHROMADB:
-            raise ImportError(
-                ""ChromaDB is required for memory storage features. ""
-                ""Please install it with 'pip install crewai[storage]'""
-            )
+            raise ChromaDBRequiredError(""memory storage"")
             
         try:
             from chromadb.utils.embedding_functions.openai_embedding_function import (
@@ -197,7 +189,4 @@ def _create_default_embedding_function(self):
                 api_key=os.getenv(""OPENAI_API_KEY""), model_name=""text-embedding-3-small""
             )
         except ImportError:
-            raise ImportError(
-                ""ChromaDB is required for memory storage features. ""
-                ""Please install it with 'pip install crewai[storage]'""
-            )
+            raise ChromaDBRequiredError(""memory storage"")