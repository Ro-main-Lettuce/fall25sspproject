@@ -37,6 +37,7 @@ class DOCXSearchTool(RagTool):
     def __init__(self, docx: Optional[str] = None, **kwargs):
         super().__init__(**kwargs)
         if docx is not None:
+            kwargs[""data_type""] = DataType.DOCX
             self.add(docx)
             self.description = f""A tool that can be used to semantic search a query the {docx} DOCX's content.""
             self.args_schema = FixedDOCXSearchToolSchema
@@ -47,7 +48,6 @@ def add(
         *args: Any,
         **kwargs: Any,
     ) -> None:
-        kwargs[""data_type""] = DataType.DOCX
         super().add(*args, **kwargs)
 
     def _before_run(