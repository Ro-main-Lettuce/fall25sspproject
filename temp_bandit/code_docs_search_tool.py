@@ -31,6 +31,7 @@ class CodeDocsSearchTool(RagTool):
     def __init__(self, docs_url: Optional[str] = None, **kwargs):
         super().__init__(**kwargs)
         if docs_url is not None:
+            kwargs[""data_type""] = DataType.DOCS_SITE
             self.add(docs_url)
             self.description = f""A tool that can be used to semantic search a query the {docs_url} Code Docs content.""
             self.args_schema = FixedCodeDocsSearchToolSchema
@@ -41,7 +42,6 @@ def add(
         *args: Any,
         **kwargs: Any,
     ) -> None:
-        kwargs[""data_type""] = DataType.DOCS_SITE
         super().add(*args, **kwargs)
 
     def _before_run(