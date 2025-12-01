@@ -13,18 +13,14 @@
 from time import sleep
 from typing import Any, Callable, Optional, Protocol, Union
 
+from ..import_utils import optional_import_block, require_optional_import
 from ..messages.base_message import BaseMessage
 from ..messages.print_message import PrintMessage
 from .base import IOStream
 
 # Check if the websockets module is available
-try:
+with optional_import_block():
     from websockets.sync.server import serve as ws_serve
-except ImportError as e:
-    _import_error: Optional[ImportError] = e
-else:
-    _import_error = None
-
 
 __all__ = (""IOWebsockets"",)
 
@@ -82,6 +78,7 @@ def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
         ...  # pragma: no cover
 
 
+@require_optional_import(""websockets"", ""websockets"")
 class IOWebsockets(IOStream):
     """"""A websocket input/output stream.""""""
 
@@ -94,9 +91,6 @@ def __init__(self, websocket: ServerConnection) -> None:
         Raises:
             ImportError: If the websockets module is not available.
         """"""
-        if _import_error is not None:
-            raise _import_error  # pragma: no cover
-
         self._websocket = websocket
 
     @staticmethod
@@ -140,9 +134,6 @@ def run_server_in_thread(
         server_dict: dict[str, WebSocketServer] = {}
 
         def _run_server() -> None:
-            if _import_error is not None:
-                raise _import_error
-
             # print(f"" - _run_server(): starting server on ws://{host}:{port}"", flush=True)
             with ws_serve(
                 handler=partial(IOWebsockets._handler, on_connect=on_connect),