@@ -1,60 +1,94 @@
 import asyncio
-
+import os
 import agentops
 from dotenv import load_dotenv
-import os
 from groq import Groq, AsyncGroq
 
 load_dotenv()
-agentops.init(default_tags=[""groq-provider-test""])
-groq_client = Groq(api_key=os.getenv(""GROQ_API_KEY""))
-async_groq_client = AsyncGroq(api_key=os.getenv(""GROQ_API_KEY""))
-
-messages = [{""role"": ""user"", ""content"": ""Hello""}]
-
-# option 1: use session.patch
-res = groq_client.chat.completions.create(
-    model=""llama3-70b-8192"",
-    messages=[
-        {""role"": ""user"", ""content"": ""Say hello""},
-    ],
-)
-
-stream_res = groq_client.chat.completions.create(
-    model=""llama3-70b-8192"",
-    messages=[
-        {""role"": ""user"", ""content"": ""Say hello""},
-    ],
-    stream=True,
-)
-
-for chunk in stream_res:
-    print(chunk)
-
-
-async def async_test():
-    async_res = await async_groq_client.chat.completions.create(
-        model=""llama3-70b-8192"",
-        messages=[
-            {""role"": ""user"", ""content"": ""Say hello""},
-        ],
-    )
-    print(async_res)
-
-
-asyncio.run(async_test())
-
-agentops.stop_instrumenting()
-
-untracked_res = groq_client.chat.completions.create(
-    model=""llama3-70b-8192"",
-    messages=[
-        {""role"": ""user"", ""content"": ""Say hello""},
-    ],
-)
-
-agentops.end_session(end_state=""Success"")
-
-###
-#  Used to verify that one session is created with one LLM event
-###
+
+def test_groq_integration():
+    """"""Integration test demonstrating all four Groq call patterns:
+    1. Sync (non-streaming)
+    2. Sync (streaming)
+    3. Async (non-streaming)
+    4. Async (streaming)
+
+    Verifies that AgentOps correctly tracks all LLM calls via analytics.
+    """"""
+    # Initialize AgentOps without auto-starting session
+    agentops.init(auto_start_session=False)
+    session = agentops.start_session()
+
+    # Initialize client and provider
+    groq_client = Groq(api_key=os.getenv(""GROQ_API_KEY""))
+    from agentops.llms.providers.groq import GroqProvider
+    provider = GroqProvider(groq_client)
+    provider.override()
+    
+    # Pass session to provider
+    provider.client = session
+    async_groq_client = AsyncGroq(api_key=os.getenv(""GROQ_API_KEY""))
+
+    def sync_no_stream():
+        groq_client.chat.completions.create(
+            model=""llama3-70b-8192"",
+            messages=[
+                {""role"": ""user"", ""content"": ""Hello from sync no stream""},
+            ],
+            session=session
+        )
+
+    def sync_stream():
+        stream_response = groq_client.chat.completions.create(
+            model=""llama3-70b-8192"",
+            messages=[
+                {""role"": ""user"", ""content"": ""Hello from sync streaming""},
+            ],
+            stream=True,
+            session=session
+        )
+        for _ in stream_response:
+            pass
+
+    async def async_no_stream():
+        await async_groq_client.chat.completions.create(
+            model=""llama3-70b-8192"",
+            messages=[
+                {""role"": ""user"", ""content"": ""Hello from async no stream""},
+            ],
+            session=session
+        )
+
+    async def async_stream():
+        async_stream_response = await async_groq_client.chat.completions.create(
+            model=""llama3-70b-8192"",
+            messages=[
+                {""role"": ""user"", ""content"": ""Hello from async streaming""},
+            ],
+            stream=True,
+            session=session
+        )
+        async for _ in async_stream_response:
+            pass
+
+    async def run_async_tests():
+        await async_no_stream()
+        await async_stream()
+
+    # Call each function with proper error handling
+    try:
+        sync_no_stream()
+        sync_stream()
+        asyncio.run(run_async_tests())
+    except Exception as e:
+        print(f""Error during Groq test: {str(e)}"")
+        raise
+
+    session.end_session(""Success"")
+    analytics = session.get_analytics()
+    print(analytics)
+    # Verify that all LLM calls were tracked
+    assert analytics[""LLM calls""] >= 4, f""Expected at least 4 LLM calls, but got {analytics['LLM calls']}""
+
+if __name__ == ""__main__"":
+    test_groq_integration()