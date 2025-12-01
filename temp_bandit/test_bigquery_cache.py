@@ -48,6 +48,9 @@ def test_decimal_type_conversion(
         assert converted_type.precision == 38, ""Precision should be 38""
         assert converted_type.scale == 9, ""Scale should be 9""
 
+        # Ensure schema exists before creating table
+        new_bigquery_cache._ensure_schema_exists()
+
         # Create a test table with a DECIMAL column
         sql = f""""""
         CREATE TABLE {new_bigquery_cache.schema_name}.{table_name} (