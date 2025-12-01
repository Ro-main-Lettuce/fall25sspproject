@@ -20,10 +20,9 @@ def test_ai21_integration():
     print(""AGENTOPS_API_KEY present:"", bool(os.getenv(""AGENTOPS_API_KEY"")))
     print(""AI21_API_KEY present:"", bool(os.getenv(""AI21_API_KEY"")))
 
-    agentops.init(auto_start_session=False, instrument_llm_calls=True)
+    # Initialize AgentOps without auto-starting session
+    agentops.init(auto_start_session=False)
     session = agentops.start_session()
-    print(""Session created:"", bool(session))
-    print(""Session ID:"", session.session_id if session else None)
 
     def sync_no_stream():
         client = AI21Client(api_key=os.getenv(""AI21_API_KEY""))
@@ -69,14 +68,12 @@ async def async_stream():
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
+    # Call each function
+    sync_no_stream()
+    sync_stream()
+    asyncio.run(async_no_stream())
+    asyncio.run(async_stream())
+    session.end_session(""Success"")
     analytics = session.get_analytics()
     print(""Final analytics:"", analytics)
     # Verify that all LLM calls were tracked