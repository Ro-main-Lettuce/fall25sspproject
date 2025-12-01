@@ -6,25 +6,18 @@
     0.005,
     0.01,
     0.025,
-    0.05,
-    0.075,  # Keep existing small buckets
+    0.05,  # Fast API calls (5ms - 50ms)
     0.1,
     0.25,
     0.5,
-    0.75,
-    1.0,
+    1.0,  # Regular API calls (100ms - 1s)
     2.5,
     5.0,
-    7.5,
-    10.0,
-    15.0,
+    10.0,  # Long API calls (2.5s - 10s)
     30.0,
-    45.0,
-    60.0,  # Add medium buckets for small/medium models
-    90.0,
+    60.0,
     120.0,
-    150.0,
-    180.0,  # Add large buckets for large models
+    180.0,  # LLM models (30s - 180s)
     INF,
 )
 