@@ -31,6 +31,7 @@ class XMLSearchTool(RagTool):
     def __init__(self, xml: Optional[str] = None, **kwargs):
         super().__init__(**kwargs)
         if xml is not None:
+            kwargs[""data_type""] = DataType.XML
             self.add(xml)
             self.description = f""A tool that can be used to semantic search a query the {xml} XML's content.""
             self.args_schema = FixedXMLSearchToolSchema
@@ -41,7 +42,6 @@ def add(
         *args: Any,
         **kwargs: Any,
     ) -> None:
-        kwargs[""data_type""] = DataType.XML
         super().add(*args, **kwargs)
 
     def _before_run(