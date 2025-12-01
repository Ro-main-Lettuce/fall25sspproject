@@ -65,7 +65,7 @@ def sync_stream():
             stream=True
         )
         for chunk in stream_response:
-            _ = chunk.choices[0].delta.content if hasattr(chunk.choices[0].delta, 'content') else ''
+            _ = chunk.choices[0].delta.content if hasattr(chunk.choices[0].delta, ""content"") else """"
 
     async def async_no_stream():
         await async_chat_client.create(