@@ -82,7 +82,7 @@ def has_updates_to_datasource(query: str) -> bool:
 
 def get_datasets_from_duckdb(
     connection: Optional[duckdb.DuckDBPyConnection],
-    engine_name: Optional[str] = None,
+    engine_name: Optional[VariableName] = None,
 ) -> List[DataTable]:
     try:
         return _get_datasets_from_duckdb_internal(connection, engine_name)
@@ -93,7 +93,7 @@ def get_datasets_from_duckdb(
 
 def _get_datasets_from_duckdb_internal(
     connection: Optional[duckdb.DuckDBPyConnection],
-    engine_name: Optional[str] = None,
+    engine_name: Optional[VariableName] = None,
 ) -> List[DataTable]:
     # Columns
     # 0:""database""
@@ -148,7 +148,7 @@ def _get_datasets_from_duckdb_internal(
                 num_columns=len(columns),
                 variable_name=None,
                 columns=columns,
-                engine=engine_name,  # type: ignore[arg-type]
+                engine=engine_name,
             )
         )
 