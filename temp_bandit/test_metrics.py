@@ -211,13 +211,15 @@ def test_default_bucket():
     # Verify DEFAULT_BUCKET covers appropriate ranges for both fast APIs and LLM workloads
     from bentoml._internal.utils.metrics import DEFAULT_BUCKET
 
-    # Test smallest bucket
-    assert DEFAULT_BUCKET[0] == 0.005  # 5ms for fast APIs
-
-    # Test largest finite bucket
-    assert DEFAULT_BUCKET[-2] == 180.0  # 180s for LLM workloads
-
-    # Test infinity is present
+    # Test bucket count
+    assert len(DEFAULT_BUCKET) == 16  # Optimized number of buckets
+
+    # Test key latency boundaries
+    assert DEFAULT_BUCKET[0] == 0.005  # Fast API calls start (5ms)
+    assert DEFAULT_BUCKET[4] == 0.1  # Regular API calls start (100ms)
+    assert DEFAULT_BUCKET[8] == 2.5  # Long API calls start (2.5s)
+    assert DEFAULT_BUCKET[11] == 30.0  # LLM models start (30s)
+    assert DEFAULT_BUCKET[-2] == 180.0  # Maximum LLM latency (180s)
     assert DEFAULT_BUCKET[-1] == float(""inf"")
 
     # Test monotonic increase