@@ -31,6 +31,7 @@ class CSVSearchTool(RagTool):
     def __init__(self, csv: Optional[str] = None, **kwargs):
         super().__init__(**kwargs)
         if csv is not None:
+            kwargs[""data_type""] = DataType.CSV
             self.add(csv)
             self.description = f""A tool that can be used to semantic search a query the {csv} CSV's content.""
             self.args_schema = FixedCSVSearchToolSchema
@@ -41,7 +42,6 @@ def add(
         *args: Any,
         **kwargs: Any,
     ) -> None:
-        kwargs[""data_type""] = DataType.CSV
         super().add(*args, **kwargs)
 
     def _before_run(