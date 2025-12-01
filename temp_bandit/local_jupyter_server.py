@@ -20,9 +20,11 @@
     from typing_extensions import Self
 
 from .base import JupyterConnectable, JupyterConnectionInfo
+from .import_utils import require_jupyter_kernel_gateway_installed
 from .jupyter_client import JupyterClient
 
 
+@require_jupyter_kernel_gateway_installed()
 class LocalJupyterServer(JupyterConnectable):
     class GenerateToken:
         pass