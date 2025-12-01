@@ -13,16 +13,14 @@
 from types import TracebackType
 from typing import Optional, Union
 
-from autogen.coding.utils import silence_pip
-
 if sys.version_info >= (3, 11):
     from typing import Self
 else:
     from typing_extensions import Self
 
-
 from ..base import CodeBlock, CodeExecutor, CodeExtractor, IPythonCodeResult
 from ..markdown_code_extractor import MarkdownCodeExtractor
+from ..utils import silence_pip
 from .base import JupyterConnectable, JupyterConnectionInfo
 from .jupyter_client import JupyterClient
 