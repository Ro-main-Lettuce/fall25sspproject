@@ -108,7 +108,8 @@ def __init__(self, request: Union[Request, WebSocket]) -> None:
 
     def get_current_session_id(self) -> Optional[SessionId]:
         """"""Get the current session.""""""
-        return self.request.headers.get(""Marimo-Session-Id"")
+        session_id = self.request.headers.get(""Marimo-Session-Id"")
+        return SessionId(session_id) if session_id is not None else None
 
     def require_current_session_id(self) -> SessionId:
         """"""Get the current session or raise an error.""""""