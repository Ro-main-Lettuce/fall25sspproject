@@ -9,13 +9,14 @@
 from collections.abc import Sequence
 from typing import Optional, Union
 
+from ....import_utils import optional_import_block, require_optional_import
 from .base import Document, ItemID, QueryResults, VectorDB
 from .utils import get_logger
 
-try:
+with optional_import_block():
+    from fastembed import TextEmbedding
     from qdrant_client import QdrantClient, models
-except ImportError:
-    raise ImportError(""Please install qdrant-client: `pip install qdrant-client`"")
+
 
 logger = get_logger(__name__)
 
@@ -28,6 +29,7 @@ def __call__(self, inputs: list[str]) -> list[Embeddings]:
         raise NotImplementedError
 
 
+@require_optional_import(""fastembed"", ""retrievechat-qdrant"")
 class FastEmbedEmbeddingFunction(EmbeddingFunction):
     """"""Embedding function implementation using FastEmbed - https://qdrant.github.io/fastembed.""""""
 
@@ -57,12 +59,6 @@ def __init__(
         Raises:
             ValueError: If the model_name is not in the format `<org>/<model>` e.g. BAAI/bge-small-en-v1.5.
         """"""
-        try:
-            from fastembed import TextEmbedding
-        except ImportError as e:
-            raise ValueError(
-                ""The 'fastembed' package is not installed. Please install it with `pip install fastembed`"",
-            ) from e
         self._batch_size = batch_size
         self._parallel = parallel
         self._model = TextEmbedding(model_name=model_name, cache_dir=cache_dir, threads=threads, **kwargs)
@@ -73,6 +69,7 @@ def __call__(self, inputs: list[str]) -> list[Embeddings]:
         return [embedding.tolist() for embedding in embeddings]
 
 
+@require_optional_import(""qdrant_client"", ""retrievechat-qdrant"")
 class QdrantVectorDB(VectorDB):
     """"""A vector database implementation that uses Qdrant as the backend.""""""
 
@@ -274,7 +271,7 @@ def _point_to_document(self, point) -> Document:
     def _points_to_documents(self, points) -> list[Document]:
         return [self._point_to_document(point) for point in points]
 
-    def _scored_point_to_document(self, scored_point: models.ScoredPoint) -> tuple[Document, float]:
+    def _scored_point_to_document(self, scored_point: ""models.ScoredPoint"") -> tuple[Document, float]:
         return self._point_to_document(scored_point), scored_point.score
 
     def _documents_to_points(self, documents: list[Document]):
@@ -293,7 +290,7 @@ def _documents_to_points(self, documents: list[Document]):
         ]
         return points
 
-    def _scored_points_to_documents(self, scored_points: list[models.ScoredPoint]) -> list[tuple[Document, float]]:
+    def _scored_points_to_documents(self, scored_points: list[""models.ScoredPoint""]) -> list[tuple[Document, float]]:
         return [self._scored_point_to_document(scored_point) for scored_point in scored_points]
 
     def _validate_update_ids(self, collection_name: str, ids: list[str]) -> bool: