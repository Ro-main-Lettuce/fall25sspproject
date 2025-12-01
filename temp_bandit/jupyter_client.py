@@ -6,7 +6,10 @@
 # SPDX-License-Identifier: MIT
 from __future__ import annotations
 
+import datetime
+import json
 import sys
+import uuid
 from dataclasses import dataclass
 from types import TracebackType
 from typing import Any, cast
@@ -16,17 +19,17 @@
 else:
     from typing_extensions import Self
 
-import datetime
-import json
-import uuid
 
 import requests
-import websocket
 from requests.adapters import HTTPAdapter, Retry
-from websocket import WebSocket
 
+from ...import_utils import optional_import_block, require_optional_import
 from .base import JupyterConnectionInfo
 
+with optional_import_block():
+    import websocket
+    from websocket import WebSocket
+
 
 class JupyterClient:
     def __init__(self, connection_info: JupyterConnectionInfo):
@@ -90,12 +93,14 @@ def restart_kernel(self, kernel_id: str) -> None:
         )
         response.raise_for_status()
 
+    @require_optional_import(""websocket"", ""jupyter-executor"")
     def get_kernel_client(self, kernel_id: str) -> JupyterKernelClient:
         ws_url = f""{self._get_ws_base_url()}/api/kernels/{kernel_id}/channels""
         ws = websocket.create_connection(ws_url, header=self._get_headers())
         return JupyterKernelClient(ws)
 
 
+@require_optional_import(""websocket"", ""jupyter-executor"")
 class JupyterKernelClient:
     """"""(Experimental) A client for communicating with a Jupyter kernel.""""""
 
@@ -110,7 +115,7 @@ class DataItem:
         output: str
         data_items: list[DataItem]
 
-    def __init__(self, websocket: WebSocket):
+    def __init__(self, websocket: ""WebSocket""):
         self._session_id: str = uuid.uuid4().hex
         self._websocket: WebSocket = websocket
 