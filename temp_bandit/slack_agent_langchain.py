@@ -48,7 +48,7 @@ def callback_new_message(event: TriggerEventData) -> None:
 
     # Ignore messages from the bot itself to prevent self-responses
     if user_id == BOT_USER_ID:
-        return ""Bot ignored""
+        return ""Bot ignored"" # type: ignore
 
     message = payload.get(""text"", """")
 
@@ -57,7 +57,7 @@ def callback_new_message(event: TriggerEventData) -> None:
         print(f""Bot not tagged, ignoring message - {message} - {BOT_USER_ID}"")
         return (
             f""Bot not tagged, ignoring message - {json.dumps(payload)} - {BOT_USER_ID}""
-        )
+        ) # type: ignore
 
     # Extract channel and timestamp information from the event payload
     channel_id = payload.get(""channel"", """")
@@ -84,4 +84,4 @@ def callback_new_message(event: TriggerEventData) -> None:
     return result[""output""]
 
 
-listener.listen()
+listener.wait_forever()