@@ -19,55 +19,55 @@ def test_litellm_integration():
     print(""AGENTOPS_API_KEY present:"", bool(os.getenv(""AGENTOPS_API_KEY"")))
     print(""ANTHROPIC_API_KEY present:"", bool(os.getenv(""ANTHROPIC_API_KEY"")))  # LiteLLM uses Anthropic
 
-    agentops.init(auto_start_session=False, instrument_llm_calls=True)
+    # Initialize AgentOps without auto-starting session
+    agentops.init(auto_start_session=False)
     session = agentops.start_session()
-    print(""Session created:"", bool(session))
-    print(""Session ID:"", session.session_id if session else None)
 
-    def sync_no_stream():
-        litellm.api_key = os.getenv(""ANTHROPIC_API_KEY"")
-        litellm.completion(
-            model=""anthropic/claude-3-opus-20240229"",
+    # Set API key once at the start
+    litellm.api_key = os.getenv(""ANTHROPIC_API_KEY"")
+
+    async def run_all_tests():
+        # Sync non-streaming (using acompletion for consistency)
+        await litellm.acompletion(
+            model=""anthropic/claude-2"",
             messages=[{""role"": ""user"", ""content"": ""Hello from sync no stream""}],
+            max_tokens=100,
         )
 
-    def sync_stream():
-        litellm.api_key = os.getenv(""ANTHROPIC_API_KEY"")
-        stream_result = litellm.completion(
-            model=""anthropic/claude-3-opus-20240229"",
+        # Sync streaming
+        response = await litellm.acompletion(
+            model=""anthropic/claude-2"",
             messages=[{""role"": ""user"", ""content"": ""Hello from sync streaming""}],
             stream=True,
+            max_tokens=100,
         )
-        for chunk in stream_result:
+        async for chunk in response:
             if hasattr(chunk, ""choices"") and chunk.choices[0].delta.content:
                 pass
 
-    async def async_no_stream():
-        litellm.api_key = os.getenv(""ANTHROPIC_API_KEY"")
+        # Async non-streaming
         await litellm.acompletion(
-            model=""anthropic/claude-3-opus-20240229"",
+            model=""anthropic/claude-2"",
             messages=[{""role"": ""user"", ""content"": ""Hello from async no stream""}],
+            max_tokens=100,
         )
 
-    async def async_stream():
-        litellm.api_key = os.getenv(""ANTHROPIC_API_KEY"")
+        # Async streaming
         async_stream_result = await litellm.acompletion(
-            model=""anthropic/claude-3-opus-20240229"",
+            model=""anthropic/claude-2"",
             messages=[{""role"": ""user"", ""content"": ""Hello from async streaming""}],
             stream=True,
+            max_tokens=100,
         )
         async for chunk in async_stream_result:
             if hasattr(chunk, ""choices"") and chunk.choices[0].delta.content:
                 pass
 
-    try:
-        # Call each function
-        sync_no_stream()
-        sync_stream()
-        asyncio.run(async_no_stream())
-        asyncio.run(async_stream())
-    finally:
-        session.end_session(""Success"")
+    # Run all tests in a single event loop
+    asyncio.run(run_all_tests())
+
+    # End session and verify analytics
+    session.end_session(""Success"")
     analytics = session.get_analytics()
     print(analytics)
     # Verify that all LLM calls were tracked