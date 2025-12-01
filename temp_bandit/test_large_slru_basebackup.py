@@ -66,11 +66,11 @@ def record(metric, **kwargs):
 
     n_txns = 500000
 
-    def setup_wrapper(env: NeonEnv):
-        return setup_tenant_template(env, n_txns)
-
     env = setup_pageserver_with_tenants(
-        neon_env_builder, f""large_slru_count-{n_tenants}-{n_txns}"", n_tenants, setup_wrapper
+        neon_env_builder,
+        f""large_slru_count-{n_tenants}-{n_txns}"",
+        n_tenants,
+        lambda env: setup_tenant_template(env, n_txns),
     )
     run_benchmark(env, pg_bin, record, duration)
 
@@ -80,10 +80,6 @@ def setup_tenant_template(env: NeonEnv, n_txns: int):
         ""gc_period"": ""0s"",  # disable periodic gc
         ""checkpoint_timeout"": ""10 years"",
         ""compaction_period"": ""0s"",  # disable periodic compaction
-        ""compaction_threshold"": 10,
-        ""compaction_target_size"": 134217728,
-        ""checkpoint_distance"": 268435456,
-        ""image_creation_threshold"": 3,
     }
 
     template_tenant, template_timeline = env.create_tenant(set_default=True)