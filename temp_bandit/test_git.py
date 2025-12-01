@@ -3,15 +3,15 @@
 from crewai.cli.git import Repository
 
 
-@pytest.fixture()
+@pytest.fixture
 def repository(fp):
     fp.register([""git"", ""--version""], stdout=""git version 2.30.0
"")
     fp.register([""git"", ""rev-parse"", ""--is-inside-work-tree""], stdout=""true
"")
     fp.register([""git"", ""fetch""], stdout="""")
     return Repository(path=""."")
 
 
-def test_init_with_invalid_git_repo(fp):
+def test_init_with_invalid_git_repo(fp) -> None:
     fp.register([""git"", ""--version""], stdout=""git version 2.30.0
"")
     fp.register(
         [""git"", ""rev-parse"", ""--is-inside-work-tree""],
@@ -23,58 +23,58 @@ def test_init_with_invalid_git_repo(fp):
         Repository(path=""invalid/path"")
 
 
-def test_is_git_not_installed(fp):
+def test_is_git_not_installed(fp) -> None:
     fp.register([""git"", ""--version""], returncode=1)
 
     with pytest.raises(
-        ValueError, match=""Git is not installed or not found in your PATH.""
+        ValueError, match=""Git is not installed or not found in your PATH."",
     ):
         Repository(path=""."")
 
 
-def test_status(fp, repository):
+def test_status(fp, repository) -> None:
     fp.register(
         [""git"", ""status"", ""--branch"", ""--porcelain""],
         stdout=""## main...origin/main [ahead 1]
"",
     )
     assert repository.status() == ""## main...origin/main [ahead 1]""
 
 
-def test_has_uncommitted_changes(fp, repository):
+def test_has_uncommitted_changes(fp, repository) -> None:
     fp.register(
         [""git"", ""status"", ""--branch"", ""--porcelain""],
         stdout=""## main...origin/main
 M somefile.txt
"",
     )
     assert repository.has_uncommitted_changes() is True
 
 
-def test_is_ahead_or_behind(fp, repository):
+def test_is_ahead_or_behind(fp, repository) -> None:
     fp.register(
         [""git"", ""status"", ""--branch"", ""--porcelain""],
         stdout=""## main...origin/main [ahead 1]
"",
     )
     assert repository.is_ahead_or_behind() is True
 
 
-def test_is_synced_when_synced(fp, repository):
+def test_is_synced_when_synced(fp, repository) -> None:
     fp.register(
-        [""git"", ""status"", ""--branch"", ""--porcelain""], stdout=""## main...origin/main
""
+        [""git"", ""status"", ""--branch"", ""--porcelain""], stdout=""## main...origin/main
"",
     )
     fp.register(
-        [""git"", ""status"", ""--branch"", ""--porcelain""], stdout=""## main...origin/main
""
+        [""git"", ""status"", ""--branch"", ""--porcelain""], stdout=""## main...origin/main
"",
     )
     assert repository.is_synced() is True
 
 
-def test_is_synced_with_uncommitted_changes(fp, repository):
+def test_is_synced_with_uncommitted_changes(fp, repository) -> None:
     fp.register(
         [""git"", ""status"", ""--branch"", ""--porcelain""],
         stdout=""## main...origin/main
 M somefile.txt
"",
     )
     assert repository.is_synced() is False
 
 
-def test_is_synced_when_ahead_or_behind(fp, repository):
+def test_is_synced_when_ahead_or_behind(fp, repository) -> None:
     fp.register(
         [""git"", ""status"", ""--branch"", ""--porcelain""],
         stdout=""## main...origin/main [ahead 1]
"",
@@ -86,15 +86,15 @@ def test_is_synced_when_ahead_or_behind(fp, repository):
     assert repository.is_synced() is False
 
 
-def test_is_synced_with_uncommitted_changes_and_ahead(fp, repository):
+def test_is_synced_with_uncommitted_changes_and_ahead(fp, repository) -> None:
     fp.register(
         [""git"", ""status"", ""--branch"", ""--porcelain""],
         stdout=""## main...origin/main [ahead 1]
 M somefile.txt
"",
     )
     assert repository.is_synced() is False
 
 
-def test_origin_url(fp, repository):
+def test_origin_url(fp, repository) -> None:
     fp.register(
         [""git"", ""remote"", ""get-url"", ""origin""],
         stdout=""https://github.com/user/repo.git
"",