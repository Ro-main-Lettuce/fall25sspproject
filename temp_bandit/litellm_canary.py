@@ -63,7 +63,7 @@ async def async_stream():
             _ = async_stream_response
         else:
             async for chunk in async_stream_response:
-                _ = chunk.choices[0].delta.content if hasattr(chunk.choices[0].delta, 'content') else ''
+                _ = chunk.choices[0].delta.content if hasattr(chunk.choices[0].delta, ""content"") else """"
 
     async def run_async_tests():
         await async_no_stream()