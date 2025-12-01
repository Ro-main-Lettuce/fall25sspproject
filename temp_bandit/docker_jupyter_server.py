@@ -17,18 +17,18 @@
 
 import docker
 
-from ..docker_commandline_code_executor import _wait_for_ready
-
 if sys.version_info >= (3, 11):
     from typing import Self
 else:
     from typing_extensions import Self
 
-
+from ..docker_commandline_code_executor import _wait_for_ready
 from .base import JupyterConnectable, JupyterConnectionInfo
+from .import_utils import require_jupyter_kernel_gateway_installed
 from .jupyter_client import JupyterClient
 
 
+@require_jupyter_kernel_gateway_installed()
 class DockerJupyterServer(JupyterConnectable):
     DEFAULT_DOCKERFILE = """"""FROM quay.io/jupyter/docker-stacks-foundation
 