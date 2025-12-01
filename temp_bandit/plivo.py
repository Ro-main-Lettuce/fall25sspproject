@@ -10,16 +10,20 @@
 
 class PlivoInputHandler(TelephonyInputHandler):
     def __init__(self, queues, websocket=None, input_types=None, mark_event_meta_data=None, turn_based_conversation=False,
-                 is_welcome_message_played=False, observable_variables=None):
+                 is_welcome_message_played=False, observable_variables=None, websocket_ready_event=None):
         super().__init__(queues, websocket, input_types, mark_event_meta_data, turn_based_conversation,
-                         is_welcome_message_played=is_welcome_message_played, observable_variables=observable_variables)
+                         is_welcome_message_played=is_welcome_message_played, observable_variables=observable_variables,
+                         websocket_ready_event=websocket_ready_event)
         self.io_provider = 'plivo'
         self.client = plivosdk.RestClient(os.getenv('PLIVO_AUTH_ID'), os.getenv('PLIVO_AUTH_TOKEN'))
 
     async def call_start(self, packet):
         start = packet['start']
         self.call_sid = start['callId']
         self.stream_sid = start['streamId']
+        if self.websocket_ready_event:
+            self.websocket_ready_event.set()
+            logger.info(f""Websocket ready event set for Plivo with stream_sid: {self.stream_sid}"")
 
     async def disconnect_stream(self):
         try: