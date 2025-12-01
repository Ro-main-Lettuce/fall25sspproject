@@ -31,15 +31,17 @@ def test_compute_reconfigure(neon_simple_env: NeonEnv):
 
     endpoint.respec_deep(
         **{
-            ""skip_pg_catalog_updates"": True,
-            ""cluster"": {
-                ""settings"": [
-                    {
-                        ""name"": ""log_line_prefix"",
-                        ""vartype"": ""string"",
-                        ""value"": TEST_LOG_LINE_PREFIX,
-                    }
-                ]
+            ""spec"": {
+                ""skip_pg_catalog_updates"": True,
+                ""cluster"": {
+                    ""settings"": [
+                        {
+                            ""name"": ""log_line_prefix"",
+                            ""vartype"": ""string"",
+                            ""value"": TEST_LOG_LINE_PREFIX,
+                        }
+                    ]
+                },
             },
         }
     )