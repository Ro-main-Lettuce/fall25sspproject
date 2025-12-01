@@ -206,7 +206,7 @@ def test_write(
     duckdb_config = {}
     if motherduck_api_key:
         duckdb_config[""motherduck_token""] = motherduck_api_key
-        duckdb_config[""custom_user_agent""] = ""airbyte_intg_test""
+        duckdb_config[""custom_user_agent""] = ""airbyte""
     con = duckdb.connect(database=config.get(""destination_path""), read_only=False, config=duckdb_config)
     with con:
         cursor = con.execute(
@@ -308,7 +308,7 @@ def test_large_number_of_writes(
     duckdb_config = {}
     if motherduck_api_key:
         duckdb_config[""motherduck_token""] = motherduck_api_key
-        duckdb_config[""custom_user_agent""] = ""airbyte_intg_test""
+        duckdb_config[""custom_user_agent""] = ""airbyte""
 
     con = duckdb.connect(database=config.get(""destination_path""), read_only=False, config=duckdb_config)
     with con: