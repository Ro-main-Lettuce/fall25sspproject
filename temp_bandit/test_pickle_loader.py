@@ -49,14 +49,7 @@ def test_cache_hit_miss(self) -> None:
 
         # Create a cache file
         cache_path = loader.build_path(""hash1"", ""Pure"")
-        cache = Cache(
-            {""var1"": ""value1""},
-            ""hash1"",
-            set(),
-            ""Pure"",
-            True,
-            {}
-        )
+        cache = Cache({""var1"": ""value1""}, ""hash1"", set(), ""Pure"", True, {})
 
         with open(cache_path, ""wb"") as f:
             pickle.dump(cache, f)
@@ -84,12 +77,7 @@ def test_load_persistent_cache(self) -> None:
         cache_path = loader.build_path(""hash1"", ""Pure"")
         # Use string directly instead of Name constructor
         original_cache = Cache(
-            {""var1"": ""value1""},
-            ""hash1"",
-            set(),
-            ""Pure"",
-            True,
-            {}
+            {""var1"": ""value1""}, ""hash1"", set(), ""Pure"", True, {}
         )
 
         with open(cache_path, ""wb"") as f:
@@ -121,12 +109,7 @@ def test_load_cache(self) -> None:
         cache_path = loader.build_path(""hash1"", ""Pure"")
         # Use string directly instead of Name constructor
         original_cache = Cache(
-            {""var1"": ""value1""},
-            ""hash1"",
-            set(),
-            ""Pure"",
-            True,
-            {}
+            {""var1"": ""value1""}, ""hash1"", set(), ""Pure"", True, {}
         )
 
         with open(cache_path, ""wb"") as f:
@@ -145,14 +128,7 @@ def test_save_cache(self) -> None:
         loader = PickleLoader(""test"", self.save_path)
 
         # Create a cache
-        cache = Cache(
-            {""var1"": ""value1""},
-            ""hash1"",
-            set(),
-            ""Pure"",
-            True,
-            {}
-        )
+        cache = Cache({""var1"": ""value1""}, ""hash1"", set(), ""Pure"", True, {})
 
         # Save the cache
         loader.save_cache(cache)
@@ -170,12 +146,7 @@ def test_save_cache(self) -> None:
 
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