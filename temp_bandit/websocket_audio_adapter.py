@@ -5,13 +5,13 @@
 import base64
 import json
 from logging import Logger
-from typing import TYPE_CHECKING, Any, Optional
-
-if TYPE_CHECKING:
-    from fastapi.websockets import WebSocket
+from typing import TYPE_CHECKING, Optional
 
+from ..realtime_events import AudioDelta, RealtimeEvent, SpeechStarted
+from ..realtime_observer import RealtimeObserver
 
-from .realtime_observer import RealtimeObserver
+if TYPE_CHECKING:
+    from ..websockets import WebSocketProtocol as WebSocket
 
 LOG_EVENT_TYPES = [
     ""error"",
@@ -44,17 +44,12 @@ def __init__(self, websocket: ""WebSocket"", *, logger: Optional[Logger] = None) -
         self.mark_queue: list[str] = []
         self.response_start_timestamp_socket: Optional[int] = None
 
-    async def on_event(self, event: dict[str, Any]) -> None:
+    async def on_event(self, event: RealtimeEvent) -> None:
         """"""Receive events from the OpenAI Realtime API, send audio back to websocket.""""""
         logger = self.logger
-        if event[""type""] in LOG_EVENT_TYPES:
-            if event[""type""] == ""error"":
-                logger.warning(f""Received event {event['type']}: {event}"")
-            else:
-                logger.info(f""Received event {event['type']}: {event}"")
-
-        if event[""type""] == ""response.audio.delta"":
-            audio_payload = base64.b64encode(base64.b64decode(event[""delta""])).decode(""utf-8"")
+
+        if isinstance(event, AudioDelta):
+            audio_payload = base64.b64encode(base64.b64decode(event.delta)).decode(""utf-8"")
             audio_delta = {""event"": ""media"", ""streamSid"": self.stream_sid, ""media"": {""payload"": audio_payload}}
             await self.websocket.send_json(audio_delta)
 
@@ -64,14 +59,14 @@ async def on_event(self, event: dict[str, Any]) -> None:
                     logger.info(f""Setting start timestamp for new response: {self.response_start_timestamp_socket}ms"")
 
             # Update last_assistant_item safely
-            if event[""item_id""]:
-                self.last_assistant_item = event[""item_id""]
+            if event.item_id:
+                self.last_assistant_item = event.item_id
 
             await self.send_mark()
 
         # Trigger an interruption. Your use case might work better using `input_audio_buffer.speech_stopped`, or combining the two.
-        if event[""type""] == ""input_audio_buffer.speech_started"":
-            logger.info(""Speech started detected."")
+        if isinstance(event, SpeechStarted):
+            logger.info(""Speech start detected."")
             if self.last_assistant_item:
                 logger.info(f""Interrupting response with id: {self.last_assistant_item}"")
                 await self.handle_speech_started_event()
@@ -138,5 +133,5 @@ async def run_loop(self) -> None:
 
 if TYPE_CHECKING:
 
-    def websocket_audio_adapter(websocket: WebSocket) -> RealtimeObserver:
+    def websocket_audio_adapter(websocket: ""WebSocket"") -> RealtimeObserver:
         return WebSocketAudioAdapter(websocket)