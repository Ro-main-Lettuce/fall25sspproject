@@ -1,22 +1,30 @@
-from typing import TYPE_CHECKING
+""""""Type definitions for ASGI applications and middleware.""""""
 
-if TYPE_CHECKING:
-    import typing as t
+import typing as t
+from typing import Any
+from typing import Dict
+from typing import Protocol
 
-    from starlette.types import ASGIApp
-    from starlette.types import Message as ASGIMessage
-    from starlette.types import Receive as ASGIReceive
-    from starlette.types import Scope as ASGIScope
-    from starlette.types import Send as ASGISend
+# Base type definitions
+ASGIApp = t.Callable[..., Any]
+ASGIMessage = Dict[str, Any]
+ASGIReceive = t.Callable[[], Any]
+ASGIScope = Dict[str, Any]
+ASGISend = t.Callable[[Dict[str, Any]], Any]
 
-    class AsgiMiddleware(t.Protocol):
-        def __call__(self, app: ASGIApp, **options: t.Any) -> ASGIApp: ...
 
-    __all__ = [
-        ""AsgiMiddleware"",
-        ""ASGIApp"",
-        ""ASGIScope"",
-        ""ASGISend"",
-        ""ASGIReceive"",
-        ""ASGIMessage"",
-    ]
+# Protocol for ASGI middleware
+class AsgiMiddleware(Protocol):
+    """"""Protocol for ASGI middleware.""""""
+
+    def __call__(self, app: ASGIApp, **kwargs: Any) -> ASGIApp: ...
+
+
+__all__ = [
+    ""AsgiMiddleware"",
+    ""ASGIApp"",
+    ""ASGIScope"",
+    ""ASGISend"",
+    ""ASGIReceive"",
+    ""ASGIMessage"",
+]