@@ -10,31 +10,29 @@
 import uuid
 from typing import Any, Callable, Literal, Optional, Union
 
-from IPython import get_ipython
-
-try:
-    import chromadb
-except ImportError as e:
-    raise ImportError(f""{e}. You can try `pip install autogen[retrievechat]`, or install `chromadb` manually."")
-from autogen.agentchat import UserProxyAgent
-from autogen.agentchat.agent import Agent
-from autogen.agentchat.contrib.vectordb.base import Document, QueryResults, VectorDB, VectorDBFactory
-from autogen.agentchat.contrib.vectordb.utils import (
-    chroma_results_to_query_results,
-    filter_results_by_distance,
-    get_logger,
-)
-from autogen.code_utils import extract_code
-from autogen.retrieve_utils import (
+from ...code_utils import extract_code
+from ...formatting_utils import colored
+from ...import_utils import optional_import_block, require_optional_import
+from ...retrieve_utils import (
     TEXT_FORMATS,
     create_vector_db_from_dir,
     get_files_from_dir,
     query_vector_db,
     split_files_to_chunks,
 )
-from autogen.token_count_utils import count_token
+from ...token_count_utils import count_token
+from .. import UserProxyAgent
+from ..agent import Agent
+from ..contrib.vectordb.base import Document, QueryResults, VectorDB, VectorDBFactory
+from ..contrib.vectordb.utils import (
+    chroma_results_to_query_results,
+    filter_results_by_distance,
+    get_logger,
+)
 
-from ...formatting_utils import colored
+with optional_import_block():
+    import chromadb
+    from IPython import get_ipython
 
 logger = get_logger(__name__)
 
@@ -91,6 +89,7 @@
 UPDATE_CONTEXT_IN_PROMPT = ""you should reply exactly `UPDATE CONTEXT`""
 
 
+@require_optional_import([""chromadb"", ""IPython""], ""retrievechat"")
 class RetrieveUserProxyAgent(UserProxyAgent):
     """"""(In preview) The Retrieval-Augmented User Proxy retrieves document chunks based on the embedding
     similarity, and sends them along with the question to the Retrieval-Augmented Assistant