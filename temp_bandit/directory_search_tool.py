@@ -31,6 +31,7 @@ class DirectorySearchTool(RagTool):
     def __init__(self, directory: Optional[str] = None, **kwargs):
         super().__init__(**kwargs)
         if directory is not None:
+            kwargs[""loader""] = DirectoryLoader(config=dict(recursive=True))
             self.add(directory)
             self.description = f""A tool that can be used to semantic search a query the {directory} directory's content.""
             self.args_schema = FixedDirectorySearchToolSchema
@@ -41,7 +42,6 @@ def add(
         *args: Any,
         **kwargs: Any,
     ) -> None:
-        kwargs[""loader""] = DirectoryLoader(config=dict(recursive=True))
         super().add(*args, **kwargs)
 
     def _before_run(