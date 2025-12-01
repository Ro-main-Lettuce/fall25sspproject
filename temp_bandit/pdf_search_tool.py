@@ -30,6 +30,7 @@ class PDFSearchTool(RagTool):
     def __init__(self, pdf: Optional[str] = None, **kwargs):
         super().__init__(**kwargs)
         if pdf is not None:
+            kwargs[""data_type""] = DataType.PDF_FILE
             self.add(pdf)
             self.description = f""A tool that can be used to semantic search a query the {pdf} PDF's content.""
             self.args_schema = FixedPDFSearchToolSchema
@@ -56,7 +57,6 @@ def add(
         *args: Any,
         **kwargs: Any,
     ) -> None:
-        kwargs[""data_type""] = DataType.PDF_FILE
         super().add(*args, **kwargs)
 
     def _before_run(