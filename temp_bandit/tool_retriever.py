@@ -16,15 +16,18 @@
 from textwrap import dedent, indent
 from typing import Optional, Union
 
-import pandas as pd
-from sentence_transformers import SentenceTransformer, util
-
 from .... import AssistantAgent, UserProxyAgent
 from ....coding import CodeExecutor, CodeExtractor, LocalCommandLineCodeExecutor, MarkdownCodeExtractor
 from ....coding.base import CodeBlock, CodeResult
+from ....import_utils import optional_import_block, require_optional_import
 from ....tools import Tool, get_function_schema, load_basemodels_if_needed
 
+with optional_import_block():
+    import pandas as pd
+    from sentence_transformers import SentenceTransformer, util
+
 
+@require_optional_import([""pandas"", ""sentence_transformers""], ""retrievechat"")
 class ToolBuilder:
     TOOL_PROMPT_DEFAULT = """"""
## Functions
 You have access to the following functions. They can be accessed from the module called 'functions' by their function names.