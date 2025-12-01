@@ -64,8 +64,8 @@ def test_ro_replica_lag(
 
     project = neon_api.create_project(pg_version)
     project_id = project[""project""][""id""]
-    log.info(""Project ID: {}"", project_id)
-    log.info(""Primary endpoint ID: {}"", project[""project""][""endpoints""][0][""id""])
+    log.info(""Project ID: %s"", project_id)
+    log.info(""Primary endpoint ID: %s"", project[""endpoints""][0][""id""])
     neon_api.wait_for_operation_to_finish(project_id)
     error_occurred = False
     try:
@@ -81,7 +81,7 @@ def test_ro_replica_lag(
             endpoint_type=""read_only"",
             settings={""pg_settings"": {""hot_standby_feedback"": ""on""}},
         )
-        log.info(""Replica endpoint ID: {}"", replica[""endpoint""][""id""])
+        log.info(""Replica endpoint ID: %s"", replica[""endpoint""][""id""])
         replica_env = master_env.copy()
         replica_env[""PGHOST""] = replica[""endpoint""][""host""]
         neon_api.wait_for_operation_to_finish(project_id)
@@ -197,8 +197,8 @@ def test_replication_start_stop(
 
     project = neon_api.create_project(pg_version)
     project_id = project[""project""][""id""]
-    log.info(""Project ID: {}"", project_id)
-    log.info(""Primary endpoint ID: {}"", project[""project""][""endpoints""][0][""id""])
+    log.info(""Project ID: %s"", project_id)
+    log.info(""Primary endpoint ID: %s"", project[""endpoints""][0][""id""])
     neon_api.wait_for_operation_to_finish(project_id)
     try:
         branch_id = project[""branch""][""id""]
@@ -215,7 +215,7 @@ def test_replication_start_stop(
                 endpoint_type=""read_only"",
                 settings={""pg_settings"": {""hot_standby_feedback"": ""on""}},
             )
-            log.info(""Replica {} endpoint ID: {}"", i + 1, replica[""endpoint""][""id""])
+            log.info(""Replica %d endpoint ID: %s"", i + 1, replica[""endpoint""][""id""])
             replicas.append(replica)
             neon_api.wait_for_operation_to_finish(project_id)
 