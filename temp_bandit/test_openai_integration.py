@@ -25,14 +25,14 @@ def test_openai_integration():
     def sync_no_stream():
         client = OpenAI(api_key=os.getenv(""OPENAI_API_KEY""))
         client.chat.completions.create(
-            model=""gpt-3.5-turbo"",
+            model=""gpt-4o-mini"",
             messages=[{""role"": ""user"", ""content"": ""Hello from sync no stream""}],
         )
 
     def sync_stream():
         client = OpenAI(api_key=os.getenv(""OPENAI_API_KEY""))
         stream_result = client.chat.completions.create(
-            model=""gpt-3.5-turbo"",
+            model=""gpt-4o-mini"",
             messages=[{""role"": ""user"", ""content"": ""Hello from sync streaming""}],
             stream=True,
         )
@@ -42,28 +42,27 @@ def sync_stream():
     async def async_no_stream():
         client = AsyncOpenAI(api_key=os.getenv(""OPENAI_API_KEY""))
         await client.chat.completions.create(
-            model=""gpt-3.5-turbo"",
+            model=""gpt-4o-mini"",
             messages=[{""role"": ""user"", ""content"": ""Hello from async no stream""}],
         )
 
     async def async_stream():
         client = AsyncOpenAI(api_key=os.getenv(""OPENAI_API_KEY""))
         async_stream_result = await client.chat.completions.create(
-            model=""gpt-3.5-turbo"",
+            model=""gpt-4o-mini"",
             messages=[{""role"": ""user"", ""content"": ""Hello from async streaming""}],
             stream=True,
         )
         async for _ in async_stream_result:
             pass
 
-    try:
-        # Call each function
-        sync_no_stream()
-        sync_stream()
-        asyncio.run(async_no_stream())
-        asyncio.run(async_stream())
-    finally:
-        session.end_session(""Success"")
+    # Call each function
+    sync_no_stream()
+    sync_stream()
+    asyncio.run(async_no_stream())
+    asyncio.run(async_stream())
+
+    session.end_session(""Success"")
     analytics = session.get_analytics()
     print(analytics)
     # Verify that all LLM calls were tracked