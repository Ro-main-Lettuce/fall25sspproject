@@ -36,6 +36,9 @@ class GithubSearchTool(RagTool):
     def __init__(self, github_repo: Optional[str] = None, **kwargs):
         super().__init__(**kwargs)
         if github_repo is not None:
+            kwargs[""data_type""] = ""github""
+            kwargs[""loader""] = GithubLoader(config={""token"": self.gh_token})
+
             self.add(repo=github_repo)
             self.description = f""A tool that can be used to semantic search a query the {github_repo} github repo's content. This is not the GitHub API, but instead a tool that can provide semantic search capabilities.""
             self.args_schema = FixedGithubSearchToolSchema
@@ -49,8 +52,6 @@ def add(
     ) -> None:
         content_types = content_types or self.content_types
 
-        kwargs[""data_type""] = ""github""
-        kwargs[""loader""] = GithubLoader(config={""token"": self.gh_token})
         super().add(f""repo:{repo} type:{','.join(content_types)}"", **kwargs)
 
     def _before_run(