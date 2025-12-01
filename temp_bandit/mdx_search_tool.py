@@ -31,6 +31,7 @@ class MDXSearchTool(RagTool):
     def __init__(self, mdx: Optional[str] = None, **kwargs):
         super().__init__(**kwargs)
         if mdx is not None:
+            kwargs[""data_type""] = DataType.MDX
             self.add(mdx)
             self.description = f""A tool that can be used to semantic search a query the {mdx} MDX's content.""
             self.args_schema = FixedMDXSearchToolSchema
@@ -41,7 +42,6 @@ def add(
         *args: Any,
         **kwargs: Any,
     ) -> None:
-        kwargs[""data_type""] = DataType.MDX
         super().add(*args, **kwargs)
 
     def _before_run(