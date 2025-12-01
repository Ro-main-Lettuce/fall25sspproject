@@ -25,14 +25,14 @@ def test_mistral_integration():
 
     def sync_no_stream():
         client = Mistral(api_key=os.getenv(""MISTRAL_API_KEY""))
-        client.chat.create(
+        client.chat.complete(
             model=""mistral-large-latest"",
             messages=[{""role"": ""user"", ""content"": ""Hello from sync no stream""}],
         )
 
     def sync_stream():
         client = Mistral(api_key=os.getenv(""MISTRAL_API_KEY""))
-        stream_result = client.chat.create_stream(
+        stream_result = client.chat.stream(
             model=""mistral-large-latest"",
             messages=[{""role"": ""user"", ""content"": ""Hello from sync streaming""}],
         )
@@ -42,14 +42,14 @@ def sync_stream():
 
     async def async_no_stream():
         client = Mistral(api_key=os.getenv(""MISTRAL_API_KEY""))
-        await client.chat.create_async(
+        await client.chat.complete_async(
             model=""mistral-large-latest"",
             messages=[{""role"": ""user"", ""content"": ""Hello from async no stream""}],
         )
 
     async def async_stream():
         client = Mistral(api_key=os.getenv(""MISTRAL_API_KEY""))
-        async_stream_result = await client.chat.create_stream_async(
+        async_stream_result = await client.chat.stream_async(
             model=""mistral-large-latest"",
             messages=[{""role"": ""user"", ""content"": ""Hello from async streaming""}],
         )