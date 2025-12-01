@@ -1,4 +1,5 @@
 # Step 1: Import necessary libraries
+import json
 import os
 from dotenv import load_dotenv
 from typing import Dict
@@ -90,7 +91,7 @@ def process_message(event: TriggerEventData, is_new_message: bool) -> None:
 
     # Ignore messages from the bot itself to prevent self-responses
     if user_id == BOT_USER_ID:
-        return ""Bot ignored""
+        return ""Bot ignored"" # type: ignore
 
     message = payload.get(""text"", """")
 
@@ -99,7 +100,7 @@ def process_message(event: TriggerEventData, is_new_message: bool) -> None:
         print(f""Bot not tagged, ignoring message - {message} - {BOT_USER_ID}"")
         return (
             f""Bot not tagged, ignoring message - {json.dumps(payload)} - {BOT_USER_ID}""
-        )
+        ) # type: ignore
 
     # Extract channel and timestamp information from the event payload
     channel_id = payload.get(""channel"", """")
@@ -186,7 +187,7 @@ def run_openai_thread(thread_id: str, message: str) -> str:
     if messages.data:
         for message_response in messages.data:
             for content in message_response.content:
-                openai_response = content.text.value
+                openai_response = content.text.value # type: ignore
                 break
             if openai_response != ""No response generated"":
                 break