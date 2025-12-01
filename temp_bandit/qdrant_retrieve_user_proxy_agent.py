@@ -7,25 +7,24 @@
 import warnings
 from typing import Callable, Literal, Optional
 
-from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
-from autogen.agentchat.contrib.vectordb.utils import (
+from ...import_utils import optional_import_block, require_optional_import
+from ...retrieve_utils import TEXT_FORMATS, get_files_from_dir, split_files_to_chunks
+from ..contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
+from ..contrib.vectordb.utils import (
     chroma_results_to_query_results,
     filter_results_by_distance,
     get_logger,
 )
-from autogen.retrieve_utils import TEXT_FORMATS, get_files_from_dir, split_files_to_chunks
 
 logger = get_logger(__name__)
 
-try:
+with optional_import_block():
     import fastembed  # noqa: F401
     from qdrant_client import QdrantClient, models
     from qdrant_client.fastembed_common import QueryResponse
-except ImportError as e:
-    logger.fatal(""Failed to import qdrant_client with fastembed. Try running 'pip install qdrant_client[fastembed]'"")
-    raise e
 
 
+@require_optional_import([""fastembed"", ""qdrant_client""], ""retrievechat-qdrant"")
 class QdrantRetrieveUserProxyAgent(RetrieveUserProxyAgent):
     def __init__(
         self,
@@ -158,10 +157,11 @@ def retrieve_docs(self, problem: str, n_results: int = 20, search_string: str =
         self._results = results
 
 
+@require_optional_import([""fastembed"", ""qdrant_client""], ""retrievechat-qdrant"")
 def create_qdrant_from_dir(
     dir_path: str,
     max_tokens: int = 4000,
-    client: QdrantClient = None,
+    client: ""QdrantClient"" = None,
     collection_name: str = ""all-my-documents"",
     chunk_mode: str = ""multi_lines"",
     must_break_at_empty_line: bool = True,
@@ -172,8 +172,8 @@ def create_qdrant_from_dir(
     extra_docs: bool = False,
     parallel: int = 0,
     on_disk: bool = False,
-    quantization_config: Optional[models.QuantizationConfig] = None,
-    hnsw_config: Optional[models.HnswConfigDiff] = None,
+    quantization_config: Optional[""models.QuantizationConfig""] = None,
+    hnsw_config: Optional[""models.HnswConfigDiff""] = None,
     payload_indexing: bool = False,
     qdrant_client_options: Optional[dict] = {},
 ):
@@ -263,15 +263,16 @@ def create_qdrant_from_dir(
         )
 
 
+@require_optional_import(""qdrant_client"", ""retrievechat-qdrant"")
 def query_qdrant(
     query_texts: list[str],
     n_results: int = 10,
-    client: QdrantClient = None,
+    client: ""QdrantClient"" = None,
     collection_name: str = ""all-my-documents"",
     search_string: str = """",
     embedding_model: str = ""BAAI/bge-small-en-v1.5"",
     qdrant_client_options: Optional[dict] = {},
-) -> list[list[QueryResponse]]:
+) -> list[list[""QueryResponse""]]:
     """"""Perform a similarity search with filters on a Qdrant collection
 
     Args: