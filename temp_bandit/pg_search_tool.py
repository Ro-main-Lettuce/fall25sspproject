@@ -23,6 +23,8 @@ class PGSearchTool(RagTool):
 
     def __init__(self, table_name: str, **kwargs):
         super().__init__(**kwargs)
+        kwargs[""data_type""] = ""postgres""
+        kwargs[""loader""] = PostgresLoader(config=dict(url=self.db_uri))
         self.add(table_name)
         self.description = f""A tool that can be used to semantic search a query the {table_name} database table's content.""
         self._generate_description()
@@ -32,8 +34,6 @@ def add(
         table_name: str,
         **kwargs: Any,
     ) -> None:
-        kwargs[""data_type""] = ""postgres""
-        kwargs[""loader""] = PostgresLoader(config=dict(url=self.db_uri))
         super().add(f""SELECT * FROM {table_name};"", **kwargs)
 
     def _run(