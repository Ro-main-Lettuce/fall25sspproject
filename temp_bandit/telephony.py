@@ -13,7 +13,7 @@
 
 class TelephonyInputHandler(DefaultInputHandler):
     def __init__(self, queues, websocket=None, input_types=None, mark_event_meta_data=None, turn_based_conversation=False,
-                 is_welcome_message_played=False, observable_variables=None):
+                 is_welcome_message_played=False, observable_variables=None, websocket_ready_event=None):
         super().__init__(queues, websocket, input_types, mark_event_meta_data, turn_based_conversation,
                          is_welcome_message_played=is_welcome_message_played, observable_variables=observable_variables)
         self.stream_sid = None
@@ -23,6 +23,7 @@ def __init__(self, queues, websocket=None, input_types=None, mark_event_meta_dat
         # self.mark_event_meta_data = mark_event_meta_data
         self.last_media_received = 0
         self.io_provider = None
+        self.websocket_ready_event = websocket_ready_event
 
     def get_stream_sid(self):
         return self.stream_sid