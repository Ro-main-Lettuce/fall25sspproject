@@ -45,7 +45,7 @@ async def sync_stream():
             messages=[ChatMessage(role=""user"", content=""Hello from sync streaming"")]
         )
         async for chunk in stream_response:
-            _ = chunk.delta.content if hasattr(chunk.delta, 'content') else ''
+            _ = chunk.delta.content if hasattr(chunk.delta, ""content"") else """"
 
     async def async_no_stream():
         # Mistral doesn't have async methods, use sync