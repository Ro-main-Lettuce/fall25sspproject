@@ -30,6 +30,8 @@ class SessionTelemetryAdapter:
 
     span: trace.Span | None = field(default=None, init=False, repr=False)  # The root span for the session
 
+    telemetry: SessionTelemetry = field(default=None,repr=False,init=False)
+
     @staticmethod
     def _ns_to_iso(ns_time: Optional[int]) -> Optional[str]:
         """"""Convert nanosecond timestamp to ISO format.""""""
@@ -72,10 +74,6 @@ def end_timestamp(self, value: Optional[str]) -> None:
 
     # ------------------------------------------------------------
 
-    @property
-    def tracer(self) -> SessionTelemetry:
-        return self._tracer
-
     def set_status(self, state: SessionState, reason: Optional[str] = None) -> None:
         """"""Update root span status based on session state.""""""
         if state.is_terminal: