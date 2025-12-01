@@ -31,6 +31,7 @@ class WebsiteSearchTool(RagTool):
     def __init__(self, website: Optional[str] = None, **kwargs):
         super().__init__(**kwargs)
         if website is not None:
+            kwargs[""data_type""] = DataType.WEB_PAGE
             self.add(website)
             self.description = f""A tool that can be used to semantic search a query from {website} website content.""
             self.args_schema = FixedWebsiteSearchToolSchema
@@ -41,7 +42,6 @@ def add(
         *args: Any,
         **kwargs: Any,
     ) -> None:
-        kwargs[""data_type""] = DataType.WEB_PAGE
         super().add(*args, **kwargs)
 
     def _before_run(