@@ -31,6 +31,7 @@ class TXTSearchTool(RagTool):
     def __init__(self, txt: Optional[str] = None, **kwargs):
         super().__init__(**kwargs)
         if txt is not None:
+            kwargs[""data_type""] = DataType.TEXT_FILE
             self.add(txt)
             self.description = f""A tool that can be used to semantic search a query the {txt} txt's content.""
             self.args_schema = FixedTXTSearchToolSchema
@@ -41,7 +42,6 @@ def add(
         *args: Any,
         **kwargs: Any,
     ) -> None:
-        kwargs[""data_type""] = DataType.TEXT_FILE
         super().add(*args, **kwargs)
 
     def _before_run(