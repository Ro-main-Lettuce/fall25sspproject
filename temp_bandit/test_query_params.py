@@ -20,6 +20,13 @@ def setUp(self) -> None:
     def test_get(self) -> None:
         assert self.params.get(""key1"") == ""value1""
         assert self.params.get(""key2"") == [""value2"", ""value3""]
+        # Test with fallback parameter
+        assert self.params.get(""non_existent"", ""fallback"") == ""fallback""
+        assert self.params.get(""non_existent"", [""fallback""]) == [""fallback""]
+        assert self.params.get(""non_existent"", None) is None
+        # Test existing keys with fallback (should return original value)
+        assert self.params.get(""key1"", ""fallback"") == ""value1""
+        assert self.params.get(""key2"", ""fallback"") == [""value2"", ""value3""]
 
     def test_get_all(self) -> None:
         assert self.params.get_all(""key1"") == [""value1""]
@@ -195,6 +202,13 @@ def setUp(self):
     def test_get(self):
         assert self.params.get(""key1"") == ""value1""
         assert self.params.get(""key2"") == [""value2"", ""value3""]
+        # Test with fallback parameter
+        assert self.params.get(""non_existent"", ""fallback"") == ""fallback""
+        assert self.params.get(""non_existent"", [""fallback""]) == [""fallback""]
+        assert self.params.get(""non_existent"", None) is None
+        # Test existing keys with fallback (should return original value)
+        assert self.params.get(""key1"", ""fallback"") == ""value1""
+        assert self.params.get(""key2"", ""fallback"") == [""value2"", ""value3""]
 
     def test_get_all(self):
         assert self.params.get_all(""key1"") == [""value1""]