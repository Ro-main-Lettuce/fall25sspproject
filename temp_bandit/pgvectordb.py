@@ -10,26 +10,22 @@
 from typing import Callable, Optional, Union
 
 import numpy as np
-from sentence_transformers import SentenceTransformer
 
+from ....import_utils import optional_import_block, require_optional_import
 from .base import Document, ItemID, QueryResults, VectorDB
 from .utils import get_logger
 
-try:
+with optional_import_block():
     import pgvector  # noqa: F401
-    from pgvector.psycopg import register_vector
-except ImportError:
-    raise ImportError(""Please install pgvector: `pip install pgvector`"")
-
-try:
     import psycopg
-except ImportError:
-    raise ImportError(""Please install pgvector: `pip install psycopg`"")
+    from pgvector.psycopg import register_vector
+    from sentence_transformers import SentenceTransformer
 
 PGVECTOR_MAX_BATCH_SIZE = os.environ.get(""PGVECTOR_MAX_BATCH_SIZE"", 40000)
 logger = get_logger(__name__)
 
 
+@require_optional_import([""psycopg"", ""sentence_transformers""], ""retrievechat-pgvector"")
 class Collection:
     """"""A Collection object for PGVector.
 
@@ -543,13 +539,14 @@ def create_collection(
         cursor.close()
 
 
+@require_optional_import([""pgvector"", ""psycopg"", ""sentence_transformers""], ""retrievechat-pgvector"")
 class PGVectorDB(VectorDB):
     """"""A vector database that uses PGVector as the backend.""""""
 
     def __init__(
         self,
         *,
-        conn: Optional[psycopg.Connection] = None,
+        conn: Optional[""psycopg.Connection""] = None,
         connection_string: Optional[str] = None,
         host: Optional[str] = None,
         port: Optional[Union[int, str]] = None,
@@ -606,15 +603,15 @@ def __init__(
 
     def establish_connection(
         self,
-        conn: Optional[psycopg.Connection] = None,
+        conn: Optional[""psycopg.Connection""] = None,
         connection_string: Optional[str] = None,
         host: Optional[str] = None,
         port: Optional[Union[int, str]] = None,
         dbname: Optional[str] = None,
         username: Optional[str] = None,
         password: Optional[str] = None,
         connect_timeout: Optional[int] = 10,
-    ) -> psycopg.Connection:
+    ) -> ""psycopg.Connection"":
         """"""Establishes a connection to a PostgreSQL database using psycopg.
 
         Args: