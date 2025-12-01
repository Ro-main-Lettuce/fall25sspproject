@@ -348,7 +348,6 @@ def test_tenant_config_patch(neon_env_builder: NeonEnvBuilder, ps_managed_by: st
 
     def assert_tenant_conf_semantically_equal(lhs, rhs):
         """"""
-        Storcon returns None for fields that are not set while the pageserver does not.
         Compare two tenant's config overrides semantically, by dropping the None values.
         """"""
         lhs = {k: v for k, v in lhs.items() if v is not None}
@@ -375,10 +374,7 @@ def assert_tenant_conf_semantically_equal(lhs, rhs):
 
     patch: dict[str, Any | None] = {
         ""gc_period"": ""3h"",
-        ""wal_receiver_protocol_override"": {
-            ""type"": ""interpreted"",
-            ""args"": {""format"": ""bincode"", ""compression"": {""zstd"": {""level"": 1}}},
-        },
+        ""gc_compaction_ratio_percent"": 10,
     }
     api.patch_tenant_config(env.initial_tenant, patch)
     tenant_conf_after_patch = api.tenant_config(env.initial_tenant).tenant_specific_overrides
@@ -391,7 +387,7 @@ def assert_tenant_conf_semantically_equal(lhs, rhs):
     assert_tenant_conf_semantically_equal(tenant_conf_after_patch, crnt_tenant_conf | patch)
     crnt_tenant_conf = tenant_conf_after_patch
 
-    patch = {""gc_period"": ""5h"", ""wal_receiver_protocol_override"": None}
+    patch = {""gc_period"": ""5h"", ""gc_compaction_ratio_percent"": None}
     api.patch_tenant_config(env.initial_tenant, patch)
     tenant_conf_after_patch = api.tenant_config(env.initial_tenant).tenant_specific_overrides
     if ps_managed_by == ""storcon"":