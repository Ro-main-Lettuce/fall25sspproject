@@ -11,10 +11,9 @@
 import tiktoken
 from termcolor import colored
 
-from autogen import token_count_utils
-from autogen.cache import AbstractCache, Cache
-from autogen.types import MessageContentType
-
+from .... import token_count_utils
+from ....cache import AbstractCache, Cache
+from ....types import MessageContentType
 from . import transforms_util
 from .text_compressors import LLMLingua, TextCompressor
 