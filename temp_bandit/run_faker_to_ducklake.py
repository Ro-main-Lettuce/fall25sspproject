@@ -4,6 +4,17 @@
 Usage (from repo root):
     poetry install
     poetry run python examples/run_faker_to_ducklake.py
+
+To test:
+
+```
+brew install duckdb
+duckdb
+> .open .cache/ducklake-dummy-db.duckdb
+> ATTACH IF NOT EXISTS 'ducklake:sqlite:.cache/metadata.db' AS ducklake_data (DATA_PATH '.cache/ducklake-data');
+> SELECT * FROM ducklake_data.main.purchases;
+> ATTACH IF NOT EXISTS 'sqlite:.cache/metadata.db' AS ducklake_metadata;
+> SELECT * FROM ducklake_metadata.ducklake_table;
 """"""
 
 from __future__ import annotations