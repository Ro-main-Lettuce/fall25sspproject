@@ -9,6 +9,7 @@
 from asyncer import asyncify
 from pydantic import BaseModel
 
+from .realtime_events import FunctionCall, RealtimeEvent
 from .realtime_observer import RealtimeObserver
 
 if TYPE_CHECKING:
@@ -22,18 +23,18 @@ def __init__(self, *, logger: Optional[""Logger""] = None) -> None:
         """"""Observer for handling function calls from the OpenAI Realtime API.""""""
         super().__init__(logger=logger)
 
-    async def on_event(self, event: dict[str, Any]) -> None:
+    async def on_event(self, event: RealtimeEvent) -> None:
         """"""Handle function call events from the OpenAI Realtime API.
 
         Args:
             event (dict[str, Any]): The event from the OpenAI Realtime API.
         """"""
-        if event[""type""] == ""response.function_call_arguments.done"":
-            self.logger.info(f""Received event: {event['type']}"", event)
+        if isinstance(event, FunctionCall):
+            self.logger.info(""Received function call event"")
             await self.call_function(
-                call_id=event[""call_id""],
-                name=event[""name""],
-                kwargs=json.loads(event[""arguments""]),
+                call_id=event.call_id,
+                name=event.name,
+                kwargs=event.arguments,
             )
 
     async def call_function(self, call_id: str, name: str, kwargs: dict[str, Any]) -> None: