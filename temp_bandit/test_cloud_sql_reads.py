@@ -33,8 +33,14 @@ def previous_job_run_id() -> int:
 @pytest.mark.parametrize(
     ""deployed_connection_id"",
     [
-        pytest.param(""c7b4d838-a612-495a-9d91-a14e477add51"", id=""Faker->Snowflake""),
-        pytest.param(""0e1d6b32-b8e3-4b68-91a3-3a314599c782"", id=""Faker->BigQuery""),
+        pytest.param(
+            ""c7b4d838-a612-495a-9d91-a14e477add51"",  # https://cloud.airbyte.com/workspaces/a0cc325a-d358-4df4-bdd4-c09d753b6afb/connections/c7b4d838-a612-495a-9d91-a14e477add51/status
+            id=""Faker->Snowflake"",
+        ),
+        pytest.param(
+            ""0e1d6b32-b8e3-4b68-91a3-3a314599c782"",  # https://cloud.airbyte.com/workspaces/a0cc325a-d358-4df4-bdd4-c09d753b6afb/connections/0e1d6b32-b8e3-4b68-91a3-3a314599c782/status
+            id=""Faker->BigQuery"",
+        ),
         pytest.param(
             """", id=""Faker->Postgres"", marks=pytest.mark.skip(reason=""Not yet supported"")
         ),
@@ -76,7 +82,11 @@ def test_read_from_deployed_connection(
 
     pandas_df = pd.DataFrame(data_as_list)
 
-    assert pandas_df.shape == (100, 20)
+    assert pandas_df.shape[0] == 100
+    assert pandas_df.shape[1] in {  # Column count diff depending on when it was created
+        20,
+        21,
+    }
 
     # Check that no values are null
     for col in pandas_df.columns:
@@ -87,12 +97,12 @@ def test_read_from_deployed_connection(
     ""deployed_connection_id, cache_type"",
     [
         pytest.param(
-            ""c7b4d838-a612-495a-9d91-a14e477add51"",
+            ""c7b4d838-a612-495a-9d91-a14e477add51"",  # https://cloud.airbyte.com/workspaces/a0cc325a-d358-4df4-bdd4-c09d753b6afb/connections/c7b4d838-a612-495a-9d91-a14e477add51/status
             SnowflakeCache,
             id=""Faker->Snowflake"",
         ),
         pytest.param(
-            ""0e1d6b32-b8e3-4b68-91a3-3a314599c782"",
+            ""0e1d6b32-b8e3-4b68-91a3-3a314599c782"",  # https://cloud.airbyte.com/workspaces/a0cc325a-d358-4df4-bdd4-c09d753b6afb/connections/0e1d6b32-b8e3-4b68-91a3-3a314599c782/status
             BigQueryCache,
             id=""Faker->BigQuery"",
         ),
@@ -185,7 +195,11 @@ def test_read_from_previous_job(
 
     pandas_df = pd.DataFrame(data_as_list)
 
-    assert pandas_df.shape == (100, 20)
+    assert pandas_df.shape[0] == 100
+    assert pandas_df.shape[1] in {  # Column count diff depending on when it was created
+        20,
+        21,
+    }
     for col in pandas_df.columns:
         # Check that no values are null
         assert pandas_df[col].notnull().all()