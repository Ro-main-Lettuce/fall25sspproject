@@ -44,14 +44,14 @@ def __init__(self, config: GatewayConfig):
         self._rate_limit_remaining = 120
         self._rate_limit_reset = 0
         
-    async def connect(self):
+    async def connect(self) -> None:
         """"""Establish WebSocket connection with Discord Gateway.""""""
         url = f""wss://gateway.discord.gg/?v={self.config.version}&encoding={self.config.encoding}""
         self.ws = await websockets.connect(url)
         await self._handle_hello()
         await self._identify()
         
-    async def _handle_hello(self):
+    async def _handle_hello(self) -> None:
         """"""Handle the HELLO event from Discord Gateway.""""""
         try:
             data = await self.ws.recv()
@@ -108,11 +108,11 @@ async def _identify(self):
             logger.error(f""Failed to send IDENTIFY event: {e}"")
             raise
             
-    async def handle_event(self, event_type: str, callback: Callable):
+    async def handle_event(self, event_type: str, callback: Callable[[Dict[str, Any]], None]) -> None:
         """"""Register event handler for specific event type.""""""
         self._handlers[event_type] = callback
         
-    async def _handle_dispatch(self, payload: Dict[str, Any]):
+    async def _handle_dispatch(self, payload: Dict[str, Any]) -> None:
         """"""Handle dispatched events from Discord Gateway.""""""
         try:
             event_type = payload.get('t')
@@ -128,7 +128,7 @@ async def _handle_dispatch(self, payload: Dict[str, Any]):
         except Exception as e:
             logger.error(f""Failed to handle dispatch event: {e}"")
             
-    async def _process_messages(self):
+    async def _process_messages(self) -> None:
         """"""Process incoming Gateway messages.""""""
         try:
             while True:
@@ -159,7 +159,7 @@ async def _process_messages(self):
             logger.error(f""Error processing messages: {e}"")
             raise
             
-    async def _heartbeat_loop(self):
+    async def _heartbeat_loop(self) -> None:
         """"""Send heartbeats at the specified interval.""""""
         try:
             while True:
@@ -171,7 +171,7 @@ async def _heartbeat_loop(self):
             logger.error(f""Error in heartbeat loop: {e}"")
             raise
             
-    async def _send_heartbeat(self):
+    async def _send_heartbeat(self) -> None:
         """"""Send heartbeat with sequence number.""""""
         try:
             if self._rate_limit_remaining <= 0:
@@ -192,7 +192,7 @@ async def _send_heartbeat(self):
             logger.error(f""Failed to send heartbeat: {e}"")
             raise
             
-    async def _handle_reconnect(self):
+    async def _handle_reconnect(self) -> None:
         """"""Handle reconnection when requested by Discord.""""""
         try:
             if self.ws:
@@ -212,7 +212,7 @@ async def _handle_reconnect(self):
             logger.error(f""Failed to reconnect: {e}"")
             raise
             
-    async def _resume(self):
+    async def _resume(self) -> None:
         """"""Resume a disconnected session.""""""
         try:
             payload = {
@@ -230,7 +230,7 @@ async def _resume(self):
             logger.error(f""Failed to resume session: {e}"")
             raise
             
-    async def _handle_invalid_session(self, resumable: bool):
+    async def _handle_invalid_session(self, resumable: bool) -> None:
         """"""Handle invalid session response.""""""
         try:
             logger.warning(f""Session invalidated, resumable: {resumable}"")