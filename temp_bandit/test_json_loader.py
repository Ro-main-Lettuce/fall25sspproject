@@ -57,7 +57,7 @@ def test_cache_hit_miss(self) -> None:
             ""stateful_refs"": [],
             ""cache_type"": ""Pure"",
             ""hit"": True,
-            ""meta"": {}
+            ""meta"": {},
         }
 
         with open(cache_path, ""w"") as f:
@@ -92,7 +92,7 @@ def test_load_persistent_cache(self) -> None:
             ""stateful_refs"": [],
             ""cache_type"": ""Pure"",
             ""hit"": True,
-            ""meta"": {}
+            ""meta"": {},
         }
 
         with open(cache_path, ""w"") as f:
@@ -139,7 +139,7 @@ def test_load_cache(self) -> None:
             ""stateful_refs"": [],
             ""cache_type"": ""Pure"",
             ""hit"": True,
-            ""meta"": {}
+            ""meta"": {},
         }
 
         with open(cache_path, ""w"") as f:
@@ -164,7 +164,7 @@ def test_save_cache(self) -> None:
             {""stateful""},
             ""Pure"",
             True,
-            {""version"": 1}
+            {""version"": 1},
         )
 
         # Save the cache
@@ -181,17 +181,14 @@ def test_save_cache(self) -> None:
         assert loaded_json[""hash""] == ""hash1""
         assert loaded_json[""cache_type""] == ""Pure""
         assert loaded_json[""hit""] is True
-        assert isinstance(loaded_json[""stateful_refs""], list)  # Should be converted to list
+        assert isinstance(
+            loaded_json[""stateful_refs""], list
+        )  # Should be converted to list
         assert loaded_json[""meta""] == {""version"": 1}
 
         # Save another cache with different type
         cache2 = Cache(
-            {""var2"": ""value2""},
-            ""hash2"",
-            set(),
-            ""Deferred"",
-            True,
-            {}
+            {""var2"": ""value2""}, ""hash2"", set(), ""Deferred"", True, {}
         )
 
         loader.save_cache(cache2)