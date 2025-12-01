@@ -69,8 +69,7 @@ def store_metadata(self, metadata: dict):
             cursor = conn.cursor()
             # IMPORTANT: If you modify the CREATE TABLE schema below,
             # you must update the expected_columns list in validate_schema()
-            # to match the new schema. Otherwise, schema validation will fail
-            # and users will need to clear their cache.
+            # to match the new schema. Otherwise, schema validation will fail.
             cursor.execute(
                 """"""
                 CREATE TABLE IF NOT EXISTS runs (