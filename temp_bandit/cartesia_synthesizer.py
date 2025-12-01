@@ -50,6 +50,7 @@ def __init__(self, voice_id, voice, model=""sonic-english"", audio_format=""mp3"", s
         self.sequence_id = 0
         self.context_ids_to_ignore = set()
         self.conversation_ended = False
+        self.audio_buffer = b''
 
     def get_engine(self):
         return self.model
@@ -204,6 +205,14 @@ async def generate(self):
             async for message in self.receiver():
                 if len(self.text_queue) > 0:
                     self.meta_info = self.text_queue.popleft()
+                elif not self.meta_info:
+                    self.meta_info = {
+                        ""sequence_id"": -1, 
+                        ""format"": ""mulaw"",
+                        ""is_first_chunk"": False,
+                        ""end_of_synthesizer_stream"": False
+                    }
+                
                 audio = """"
 
                 if self.use_mulaw:
@@ -221,14 +230,14 @@ async def generate(self):
                     self.meta_info[""is_first_chunk""] = False
 
                 if self.last_text_sent:
-                    # Reset the last_text_sent and first_chunk converted to reset synth latency
                     self.first_chunk_generated = False
                     self.last_text_sent = True
 
                 if message == b'\x00':
                     logger.info(""received null byte and hence end of stream"")
                     self.meta_info[""end_of_synthesizer_stream""] = True
                     self.first_chunk_generated = False
+                    self.audio_buffer = b''
 
                 yield create_ws_data_packet(audio, self.meta_info)
 
@@ -269,7 +278,7 @@ async def push(self, message):
             if not self.context_id:
                 self.update_context(meta_info)
             else:
-                if self.turn_id != meta_info.get('turn_id', 0) or self.sequence_id != meta_info.get('sequence_id', 0):
+                if self.turn_id != meta_info.get('turn_id', 0):
                     self.update_context(meta_info)
 
             self.sender_task = asyncio.create_task(self.sender(text, meta_info.get('sequence_id'), end_of_llm_stream))