@@ -524,9 +524,9 @@ def _ensure_schema_exists(
 
         if DEBUG_MODE:
             found_schemas = schemas_list
-            assert schema_name in found_schemas, (
-                f""Schema {schema_name} was not created. Found: {found_schemas}""
-            )
+            assert (
+                schema_name in found_schemas
+            ), f""Schema {schema_name} was not created. Found: {found_schemas}""
 
     def _quote_identifier(self, identifier: str) -> str:
         """"""Return the given identifier, quoted.""""""