@@ -18,10 +18,9 @@ def test_anthropic_integration():
     """"""
     print(""AGENTOPS_API_KEY present:"", bool(os.getenv(""AGENTOPS_API_KEY"")))
     print(""ANTHROPIC_API_KEY present:"", bool(os.getenv(""ANTHROPIC_API_KEY"")))
-    agentops.init(auto_start_session=False, instrument_llm_calls=True)
+    # Initialize AgentOps without auto-starting session
+    agentops.init(auto_start_session=False)
     session = agentops.start_session()
-    print(""Session created:"", bool(session))
-    print(""Session ID:"", session.session_id if session else None)
 
     def sync_no_stream():
         client = Anthropic(api_key=os.getenv(""ANTHROPIC_API_KEY""))
@@ -61,14 +60,12 @@ async def async_stream():
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
+    session.end_session(""Success"")
     analytics = session.get_analytics()
     print(analytics)
     # Verify that all LLM calls were tracked