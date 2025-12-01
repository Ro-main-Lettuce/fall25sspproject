@@ -7,6 +7,7 @@
 @dataclass
 class GitCommitInfo:
     """"""Information about a git commit.""""""
+
     commit_hash: str
     author: str
     date: datetime
@@ -18,10 +19,4 @@ def from_commit(cls, commit: Commit, filepath: str) -> ""GitCommitInfo | None"":
         stats = commit.stats.files.get(filepath)
         if not stats:
             return None
-        return cls(
-            commit_hash=commit.hexsha,
-            author=commit.author.name or ""Unknown"",
-            date=commit.committed_datetime,
-            lines_added=stats[""insertions""],
-            lines_removed=stats[""deletions""]
-        )
+        return cls(commit_hash=commit.hexsha, author=commit.author.name or ""Unknown"", date=commit.committed_datetime, lines_added=stats[""insertions""], lines_removed=stats[""deletions""])