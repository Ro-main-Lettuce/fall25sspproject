@@ -46,7 +46,7 @@
 ]
 
 agent = FunctionCallingAgentWorker(
-    tools=composio_tools,
+    tools=list(composio_tools), # type: ignore
     llm=llm,
     prefix_messages=prefix_messages,
     max_function_calls=10,
@@ -64,7 +64,7 @@ def callback_new_message(event: TriggerEventData) -> None:
 
     # Ignore messages from the bot itself to prevent self-responses
     if user_id == BOT_USER_ID:
-        return ""Bot ignored""
+        return ""Bot ignored"" # type: ignore
 
     message = payload.get(""text"", """")
 
@@ -73,7 +73,7 @@ def callback_new_message(event: TriggerEventData) -> None:
         print(f""Bot not tagged, ignoring message - {message} - {BOT_USER_ID}"")
         return (
             f""Bot not tagged, ignoring message - {json.dumps(payload)} - {BOT_USER_ID}""
-        )
+        ) # type: ignore
 
     # Extract channel and timestamp information from the event payload
     channel_id = payload.get(""channel"", """")
@@ -92,4 +92,4 @@ def callback_new_message(event: TriggerEventData) -> None:
     )
 
 
-listener.listen()
+listener.wait_forever()
\ No newline at end of file