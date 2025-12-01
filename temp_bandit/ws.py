@@ -291,7 +291,7 @@ def __init__(
         self.message_queue: asyncio.Queue[KernelMessage]
         self.ws_future: asyncio.Future[tuple[None, None]] | None = None
 
-        super().__init__(consumer_id=ConsumerId(str(session_id)))
+        super().__init__(consumer_id=ConsumerId(session_id))
 
     def _write_kernel_ready(
         self,
@@ -578,7 +578,7 @@ def get_session() -> Session:
 
             # 4. Handle resume
             resumable_session = mgr.maybe_resume_session(
-                SessionId(session_id), self.file_key
+                session_id, self.file_key
             )
             if resumable_session is not None:
                 LOGGER.debug(""Resuming session %s"", session_id)