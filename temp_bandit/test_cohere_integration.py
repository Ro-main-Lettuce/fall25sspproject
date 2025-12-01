@@ -21,23 +21,24 @@ def test_cohere_integration():
     print(""AGENTOPS_API_KEY present:"", bool(os.getenv(""AGENTOPS_API_KEY"")))
     print(""COHERE_API_KEY present:"", bool(os.getenv(""COHERE_API_KEY"")))
 
-    agentops.init(auto_start_session=False, instrument_llm_calls=True)
+    # Initialize AgentOps without auto-starting session
+    agentops.init(auto_start_session=False)
     session = agentops.start_session()
-    print(""Session created:"", bool(session))
-    print(""Session ID:"", session.session_id if session else None)
 
     def sync_no_stream():
         client = cohere.Client(api_key=os.getenv(""COHERE_API_KEY""))
         client.chat(
             message=""Hello from sync no stream"",
-            model=""command-r-plus"",
+            model=""command"",
+            max_tokens=100,
         )
 
     def sync_stream():
         client = cohere.Client(api_key=os.getenv(""COHERE_API_KEY""))
         stream_result = client.chat(
             message=""Hello from sync streaming"",
-            model=""command-r-plus"",
+            model=""command"",
+            max_tokens=100,
             stream=True,
         )
         for chunk in stream_result:
@@ -52,14 +53,16 @@ async def async_no_stream():
         client = cohere.AsyncClient(api_key=os.getenv(""COHERE_API_KEY""))
         await client.chat(
             message=""Hello from async no stream"",
-            model=""command-r-plus"",
+            model=""command"",
+            max_tokens=100,
         )
 
     async def async_stream():
         client = cohere.AsyncClient(api_key=os.getenv(""COHERE_API_KEY""))
         async_stream_result = await client.chat(
             message=""Hello from async streaming"",
-            model=""command-r-plus"",
+            model=""command"",
+            max_tokens=100,
             stream=True,
         )
         async for chunk in async_stream_result:
@@ -70,14 +73,12 @@ async def async_stream():
             elif isinstance(chunk, ChatStreamEndEvent):
                 break
 
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
+    session.end_session(""Success"")
     analytics = session.get_analytics()
     print(analytics)
     # Verify that all LLM calls were tracked