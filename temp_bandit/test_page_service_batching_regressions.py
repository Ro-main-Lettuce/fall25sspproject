@@ -16,6 +16,7 @@ def patch_pageserver_toml(config):
             ""mode"": ""pipelined"",
             ""max_batch_size"": 32,
             ""execution"": ""concurrent-futures"",
+            ""batching"": ""uniform-lsn"",
         }
 
     neon_env_builder.pageserver_config_override = patch_pageserver_toml