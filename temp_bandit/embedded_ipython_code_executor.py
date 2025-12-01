@@ -13,16 +13,22 @@
 from queue import Empty
 from typing import Any
 
-from jupyter_client import KernelManager  # type: ignore[attr-defined]
-from jupyter_client.kernelspec import KernelSpecManager
 from pydantic import BaseModel, Field, field_validator
 
+from ...import_utils import optional_import_block, require_optional_import
 from ..base import CodeBlock, CodeExtractor, IPythonCodeResult
 from ..markdown_code_extractor import MarkdownCodeExtractor
+from .import_utils import require_jupyter_kernel_gateway_installed
 
-__all__ = ""EmbeddedIPythonCodeExecutor""
+with optional_import_block():
+    from jupyter_client import KernelManager  # type: ignore[attr-defined]
+    from jupyter_client.kernelspec import KernelSpecManager
 
+__all__ = [""EmbeddedIPythonCodeExecutor""]
 
+
+@require_optional_import(""jupyter_client"", ""jupyter-executor"")
+@require_jupyter_kernel_gateway_installed()
 class EmbeddedIPythonCodeExecutor(BaseModel):
     """"""(Experimental) A code executor class that executes code statefully using an embedded
     IPython kernel managed by this class.