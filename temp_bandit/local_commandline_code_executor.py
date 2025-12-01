@@ -18,15 +18,14 @@
 
 from typing_extensions import ParamSpec
 
-from autogen.coding.func_with_reqs import (
+from ..code_utils import PYTHON_VARIANTS, TIMEOUT_MSG, WIN32, _cmd
+from .base import CodeBlock, CodeExecutor, CodeExtractor, CommandLineCodeResult
+from .func_with_reqs import (
     FunctionWithRequirements,
     FunctionWithRequirementsStr,
     _build_python_functions_file,
     to_stub,
 )
-
-from ..code_utils import PYTHON_VARIANTS, TIMEOUT_MSG, WIN32, _cmd
-from .base import CodeBlock, CodeExecutor, CodeExtractor, CommandLineCodeResult
 from .markdown_code_extractor import MarkdownCodeExtractor
 from .utils import _get_file_name_from_content, silence_pip
 