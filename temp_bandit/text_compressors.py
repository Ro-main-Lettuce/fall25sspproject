@@ -4,15 +4,12 @@
 #
 # Portions derived from  https://github.com/microsoft/autogen are under the MIT License.
 # SPDX-License-Identifier: MIT
-from typing import Any, Optional, Protocol
+from typing import Any, Protocol
 
-IMPORT_ERROR: Optional[Exception] = None
-try:
+from ....import_utils import optional_import_block, require_optional_import
+
+with optional_import_block() as result:
     import llmlingua
-except ImportError:
-    IMPORT_ERROR = ImportError(""LLMLingua is not installed. Please install it with `pip install autogen[long-context]`"")
-    PromptCompressor = object
-else:
     from llmlingua import PromptCompressor
 
 
@@ -27,6 +24,7 @@ def compress_text(self, text: str, **compression_params) -> dict[str, Any]:
         ...
 
 
+@require_optional_import(""llmlingua"", ""long-context"")
 class LLMLingua:
     """"""Compresses text messages using LLMLingua for improved efficiency in processing and response generation.
 
@@ -55,9 +53,6 @@ def __init__(
         Raises:
             ImportError: If the llmlingua library is not installed.
         """"""
-        if IMPORT_ERROR:
-            raise IMPORT_ERROR
-
         self._prompt_compressor = PromptCompressor(**prompt_compressor_kwargs)
 
         assert isinstance(self._prompt_compressor, llmlingua.PromptCompressor)