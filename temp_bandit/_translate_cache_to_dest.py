@@ -100,17 +100,21 @@ def snowflake_cache_to_destination_configuration(
     cache: SnowflakeCache,
 ) -> DestinationSnowflake:
     """"""Get the destination configuration from the Snowflake cache.""""""
-    return DestinationSnowflake(
-        host=f""{cache.account}.snowflakecomputing.com"",
-        database=cache.get_database_name().upper(),
-        schema=cache.schema_name.upper(),
-        warehouse=cache.warehouse,
-        role=cache.role,
-        username=cache.username,
-        credentials=UsernameAndPassword(
+    config = {
+        ""host"": f""{cache.account}.snowflakecomputing.com"",
+        ""database"": cache.get_database_name().upper(),
+        ""schema"": cache.schema_name.upper(),
+        ""warehouse"": cache.warehouse,
+        ""role"": cache.role,
+        ""username"": cache.username,
+    }
+
+    if cache.password:
+        config[""credentials""] = UsernameAndPassword(
             password=cache.password,
-        ),
-    )
+        )
+
+    return DestinationSnowflake(**config)
 
 
 def bigquery_cache_to_destination_configuration(