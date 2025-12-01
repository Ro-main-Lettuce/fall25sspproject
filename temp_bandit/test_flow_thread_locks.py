@@ -157,3 +157,26 @@ def test_flow_with_async_locks():
     result = asyncio.run(flow.kickoff_async())
     assert result == ""step 1 -> step 2""
     assert flow.state.value == ""step 1 -> step 2""
+
+
+def test_flow_concurrent_access():
+    """"""Test Flow with concurrent access.""""""
+    flow = LockFlow()
+    results = []
+    errors = []
+    
+    async def run_flow():
+        try:
+            result = await flow.kickoff_async()
+            results.append(result)
+        except Exception as e:
+            errors.append(e)
+    
+    async def test():
+        tasks = [run_flow() for _ in range(10)]
+        await asyncio.gather(*tasks)
+    
+    asyncio.run(test())
+    assert len(results) == 10
+    assert not errors
+    assert all(result == ""step 1 -> step 2"" for result in results)