@@ -251,7 +251,7 @@ def test_multiple_subscription_branching(neon_simple_env: NeonEnv):
     NUMBER_OF_DBS = 5
 
     # Create and start endpoint so that neon_local put all the generated
-    # stuff into the spec.json file.
+    # stuff into the config.json file.
     endpoint = env.endpoints.create_start(
         ""main"",
         config_lines=[
@@ -280,13 +280,15 @@ def test_multiple_subscription_branching(neon_simple_env: NeonEnv):
             }
         )
 
-    # Update the spec.json file to create the databases
+    # Update the config.json file to create the databases
     # and reconfigure the endpoint to apply the changes.
     endpoint.respec_deep(
         **{
-            ""skip_pg_catalog_updates"": False,
-            ""cluster"": {
-                ""databases"": TEST_DB_NAMES,
+            ""spec"": {
+                ""skip_pg_catalog_updates"": False,
+                ""cluster"": {
+                    ""databases"": TEST_DB_NAMES,
+                },
             },
         }
     )