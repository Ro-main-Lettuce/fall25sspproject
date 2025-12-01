@@ -7,18 +7,21 @@
 from collections.abc import Iterable, Mapping
 from copy import deepcopy
 from time import monotonic, sleep
-from typing import Any, Callable, Literal, Union
+from typing import Any, Callable, Literal, Optional, Union
 
 import numpy as np
-from pymongo import MongoClient, UpdateOne, errors
-from pymongo.collection import Collection
-from pymongo.driver_info import DriverInfo
-from pymongo.operations import SearchIndexModel
-from sentence_transformers import SentenceTransformer
 
+from ....import_utils import optional_import_block, require_optional_import
 from .base import Document, ItemID, QueryResults, VectorDB
 from .utils import get_logger
 
+with optional_import_block():
+    from pymongo import MongoClient, UpdateOne, errors
+    from pymongo.collection import Collection
+    from pymongo.driver_info import DriverInfo
+    from pymongo.operations import SearchIndexModel
+    from sentence_transformers import SentenceTransformer
+
 logger = get_logger(__name__)
 
 DEFAULT_INSERT_BATCH_SIZE = 100_000
@@ -31,14 +34,15 @@ def with_id_rename(docs: Iterable) -> list[dict[str, Any]]:
     return [{**{k: v for k, v in d.items() if k != ""_id""}, ""id"": d[""_id""]} for d in docs]
 
 
+@require_optional_import([""pymongo"", ""sentence_transformers""], ""retrievechat-mongodb"")
 class MongoDBAtlasVectorDB(VectorDB):
     """"""A Collection object for MongoDB.""""""
 
     def __init__(
         self,
         connection_string: str = """",
         database_name: str = ""vector_db"",
-        embedding_function: Callable = SentenceTransformer(""all-MiniLM-L6-v2"").encode,
+        embedding_function: Optional[Callable] = None,
         collection_name: str = None,
         index_name: str = ""vector_index"",
         overwrite: bool = False,
@@ -60,7 +64,7 @@ def __init__(
             wait_until_document_ready: float | None | Blocking call to wait until the
                 database indexes are ready. None, the default, means no wait.
         """"""
-        self.embedding_function = embedding_function
+        self.embedding_function = embedding_function or SentenceTransformer(""all-MiniLM-L6-v2"").encode
         self.index_name = index_name
         self._wait_until_index_ready = wait_until_index_ready
         self._wait_until_document_ready = wait_until_document_ready
@@ -82,7 +86,7 @@ def __init__(
         else:
             self.active_collection = None
 
-    def _is_index_ready(self, collection: Collection, index_name: str):
+    def _is_index_ready(self, collection: ""Collection"", index_name: str):
         """"""Check for the index name in the list of available search indexes to see if the
         specified index is of status READY
 
@@ -98,7 +102,7 @@ def _is_index_ready(self, collection: Collection, index_name: str):
                 return True
         return False
 
-    def _wait_for_index(self, collection: Collection, index_name: str, action: str = ""create""):
+    def _wait_for_index(self, collection: ""Collection"", index_name: str, action: str = ""create""):
         """"""Waits for the index action to be completed. Otherwise throws a TimeoutError.
 
         Timeout set on instantiation.
@@ -115,7 +119,7 @@ def _wait_for_index(self, collection: Collection, index_name: str, action: str =
 
         raise TimeoutError(f""Index {self.index_name} is not ready!"")
 
-    def _wait_for_document(self, collection: Collection, index_name: str, doc: Document):
+    def _wait_for_document(self, collection: ""Collection"", index_name: str, doc: Document):
         start = monotonic()
         while monotonic() - start < self._wait_until_document_ready:
             query_result = _vector_search(
@@ -146,7 +150,7 @@ def create_collection(
         collection_name: str,
         overwrite: bool = False,
         get_or_create: bool = True,
-    ) -> Collection:
+    ) -> ""Collection"":
         """"""Create a collection in the vector database and create a vector search index in the collection.
 
         Args:
@@ -172,7 +176,7 @@ def create_collection(
             # get_or_create is False and the collection already exists, raise an error.
             raise ValueError(f""Collection {collection_name} already exists."")
 
-    def create_index_if_not_exists(self, index_name: str = ""vector_index"", collection: Collection = None) -> None:
+    def create_index_if_not_exists(self, index_name: str = ""vector_index"", collection: ""Collection"" = None) -> None:
         """"""Creates a vector search index on the specified collection in MongoDB.
 
         Args:
@@ -182,7 +186,7 @@ def create_index_if_not_exists(self, index_name: str = ""vector_index"", collectio
         if not self._is_index_ready(collection, index_name):
             self.create_vector_search_index(collection, index_name)
 
-    def get_collection(self, collection_name: str = None) -> Collection:
+    def get_collection(self, collection_name: str = None) -> ""Collection"":
         """"""Get the collection from the vector database.
 
         Args:
@@ -218,7 +222,7 @@ def delete_collection(self, collection_name: str) -> None:
 
     def create_vector_search_index(
         self,
-        collection: Collection,
+        collection: ""Collection"",
         index_name: Union[str, None] = ""vector_index"",
         similarity: Literal[""euclidean"", ""cosine"", ""dotProduct""] = ""cosine"",
     ) -> None:
@@ -334,7 +338,7 @@ def insert_docs(
                 self._wait_for_document(collection, self.index_name, docs[-1])
 
     def _insert_batch(
-        self, collection: Collection, texts: list[str], metadatas: list[Mapping[str, Any]], ids: list[ItemID]
+        self, collection: ""Collection"", texts: list[str], metadatas: list[Mapping[str, Any]], ids: list[ItemID]
     ) -> set[ItemID]:
         """"""Compute embeddings for and insert a batch of Documents into the Collection.
 
@@ -500,7 +504,7 @@ def retrieve_docs(
 def _vector_search(
     embedding_vector: list[float],
     n_results: int,
-    collection: Collection,
+    collection: ""Collection"",
     index_name: str,
     distance_threshold: float = -1.0,
     oversampling_factor=10,