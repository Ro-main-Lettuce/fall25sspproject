@@ -53,10 +53,9 @@ def test_sampling_pii_disabled(test_id: str, dbt_project: DbtProject):
 
 
 @pytest.mark.skip_targets([""clickhouse""])
-def test_sampling_pii_disabled_with_default_config(
+def test_sampling_pii_disabled_with_default_config_and_casing(
     test_id: str, dbt_project: DbtProject
 ):
-    """"""Test that PII-tagged tables don't upload samples even when tests fail""""""
     null_count = 50
     data = [{COLUMN_NAME: None} for _ in range(null_count)]
 
@@ -66,7 +65,7 @@ def test_sampling_pii_disabled_with_default_config(
         dict(column_name=COLUMN_NAME),
         data=data,
         as_model=True,
-        model_config={""config"": {""tags"": [""pii""]}},
+        model_config={""config"": {""tags"": [""pIi""]}},
         test_vars={
             ""enable_elementary_test_materialization"": True,
             ""test_sample_row_count"": TEST_SAMPLE_ROW_COUNT,