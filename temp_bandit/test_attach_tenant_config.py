@@ -155,6 +155,7 @@ def test_fully_custom_config(positive_env: NeonEnv):
         ""compaction_algorithm"": {
             ""kind"": ""tiered"",
         },
+        ""compaction_shard_ancestor"": False,
         ""eviction_policy"": {
             ""kind"": ""LayerAccessThreshold"",
             ""period"": ""20s"",
@@ -187,6 +188,7 @@ def test_fully_custom_config(positive_env: NeonEnv):
         },
         ""rel_size_v2_enabled"": False,  # test suite enables it by default as of https://github.com/neondatabase/neon/issues/11081, so, custom config means disabling it
         ""gc_compaction_enabled"": True,
+        ""gc_compaction_verification"": False,
         ""gc_compaction_initial_threshold_kb"": 1024000,
         ""gc_compaction_ratio_percent"": 200,
         ""image_creation_preempt_threshold"": 5,