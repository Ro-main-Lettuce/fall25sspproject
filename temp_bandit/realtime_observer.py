@@ -4,11 +4,12 @@
 
 from abc import ABC, abstractmethod
 from logging import Logger, getLogger
-from typing import TYPE_CHECKING, Any, Optional
+from typing import TYPE_CHECKING, Optional
 
 from anyio import Event
 
-from .realtime_client import RealtimeClientProtocol
+from .clients.realtime_client import RealtimeClientProtocol
+from .realtime_events import RealtimeEvent
 
 if TYPE_CHECKING:
     from .realtime_agent import RealtimeAgent
@@ -84,7 +85,7 @@ async def wait_for_ready(self) -> None:
         await self._ready_event.wait()
 
     @abstractmethod
-    async def on_event(self, event: dict[str, Any]) -> None:
+    async def on_event(self, event: RealtimeEvent) -> None:
         """"""Handle an event from the OpenAI Realtime API.
 
         Args: