@@ -143,10 +143,10 @@ def __init__(self, assistant_name, task_id, task, ws, input_parameters=None, con
             else:
                 self.should_record = self.task_config[""tools_config""][""output""][""provider""] == 'default' and self.enforce_streaming #In this case, this is a websocket connection and we should record
 
-            await self.__setup_output_handlers(turn_based_conversation, output_queue)
-            await self.__setup_input_handlers(turn_based_conversation, input_queue, self.should_record)
+            asyncio.create_task(self.__setup_output_handlers(turn_based_conversation, output_queue))
+            asyncio.create_task(self.__setup_input_handlers(turn_based_conversation, input_queue, self.should_record))
         else:
-            await self.__setup_output_handlers(turn_based_conversation, output_queue)
+            asyncio.create_task(self.__setup_output_handlers(turn_based_conversation, output_queue))
 
         # Agent stuff
         # Need to maintain current conversation history and overall persona/history kinda thing.