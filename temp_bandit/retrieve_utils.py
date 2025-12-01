@@ -6,34 +6,35 @@
 # SPDX-License-Identifier: MIT
 import glob
 import hashlib
+import logging
 import os
 import re
 from typing import Callable, Union
 from urllib.parse import urlparse
 
-import chromadb
-import markdownify
 import requests
-from bs4 import BeautifulSoup
 
-if chromadb.__version__ < ""0.4.15"":
-    from chromadb.api import API
-else:
-    from chromadb.api import ClientAPI as API  # noqa: N814
-import logging
+from .import_utils import optional_import_block, require_optional_import
+from .token_count_utils import count_token
 
-import chromadb.utils.embedding_functions as ef
-import pypdf
-from chromadb.api.types import QueryResult
+with optional_import_block():
+    import chromadb
+    import markdownify
+    from bs4 import BeautifulSoup
+
+    if chromadb.__version__ < ""0.4.15"":
+        from chromadb.api import API
+    else:
+        from chromadb.api import ClientAPI as API  # noqa: N814
+    import chromadb.utils.embedding_functions as ef
+    import pypdf
+    from chromadb.api.types import QueryResult
 
-from autogen.token_count_utils import count_token
 
-try:
+with optional_import_block() as result:
     from unstructured.partition.auto import partition
 
-    HAS_UNSTRUCTURED = True
-except ImportError:
-    HAS_UNSTRUCTURED = False
+HAS_UNSTRUCTURED = result.is_successful
 
 logger = logging.getLogger(__name__)
 TEXT_FORMATS = [
@@ -136,6 +137,7 @@ def split_text_to_chunks(
     return chunks
 
 
+@require_optional_import(""pypdf"", ""retrievechat"")
 def extract_text_from_pdf(file: str) -> str:
     """"""Extract text from PDF files""""""
     text = """"
@@ -251,6 +253,7 @@ def get_files_from_dir(dir_path: Union[str, list[str]], types: list = TEXT_FORMA
     return files
 
 
+@require_optional_import([""markdownify"", ""bs4""], ""retrievechat"")
 def parse_html_to_markdown(html: str, url: str = None) -> str:
     """"""Parse HTML to markdown.""""""
     soup = BeautifulSoup(html, ""html.parser"")
@@ -339,10 +342,11 @@ def is_url(string: str):
         return False
 
 
+@require_optional_import(""chromadb"", ""retrievechat"")
 def create_vector_db_from_dir(
     dir_path: Union[str, list[str]],
     max_tokens: int = 4000,
-    client: API = None,
+    client: ""API"" = None,
     db_path: str = ""tmp/chromadb.db"",
     collection_name: str = ""all-my-documents"",
     get_or_create: bool = False,
@@ -354,7 +358,7 @@ def create_vector_db_from_dir(
     custom_text_types: list[str] = TEXT_FORMATS,
     recursive: bool = True,
     extra_docs: bool = False,
-) -> API:
+) -> ""API"":
     """"""Create a vector db from all the files in a given directory, the directory can also be a single file or a url to
         a single file. We support chromadb compatible APIs to create the vector db, this function is not required if
         you prepared your own vector db.
@@ -431,16 +435,17 @@ def create_vector_db_from_dir(
     return client
 
 
+@require_optional_import(""chromadb"", ""retrievechat"")
 def query_vector_db(
     query_texts: list[str],
     n_results: int = 10,
-    client: API = None,
+    client: ""API"" = None,
     db_path: str = ""tmp/chromadb.db"",
     collection_name: str = ""all-my-documents"",
     search_string: str = """",
     embedding_model: str = ""all-MiniLM-L6-v2"",
     embedding_function: Callable = None,
-) -> QueryResult:
+) -> ""QueryResult"":
     """"""Query a vector db. We support chromadb compatible APIs, it's not required if you prepared your own vector db
         and query function.
 