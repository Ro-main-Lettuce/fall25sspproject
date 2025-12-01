@@ -138,7 +138,7 @@ def test_cli_start_stop(neon_env_builder: NeonEnvBuilder):
     env.neon_cli.pageserver_stop(env.pageserver.id)
     env.neon_cli.safekeeper_stop()
     env.neon_cli.storage_controller_stop(False)
-    env.neon_cli.object_storage_stop(False)
+    env.neon_cli.endpoint_storage_stop(False)
     env.neon_cli.storage_broker_stop()
 
     # Keep NeonEnv state up to date, it usually owns starting/stopping services
@@ -185,7 +185,7 @@ def test_cli_start_stop_multi(neon_env_builder: NeonEnvBuilder):
     env.neon_cli.safekeeper_stop(neon_env_builder.safekeepers_id_start + 1)
     env.neon_cli.safekeeper_stop(neon_env_builder.safekeepers_id_start + 2)
 
-    env.neon_cli.object_storage_stop(False)
+    env.neon_cli.endpoint_storage_stop(False)
 
     # Stop this to get out of the way of the following `start`
     env.neon_cli.storage_controller_stop(False)