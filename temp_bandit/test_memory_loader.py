@@ -30,7 +30,9 @@ def test_init_with_custom_cache(self) -> None:
         """"""Test initialization with a custom cache.""""""
         custom_cache = OrderedDict()
         loader = MemoryLoader(""test"", cache=custom_cache)
-        assert id(loader._cache) != id(custom_cache)  # Should be a copy, not the same instance
+        assert id(loader._cache) != id(
+            custom_cache
+        )  # Should be a copy, not the same instance
         assert len(loader._cache) == 0
 
     def test_cache_hit_miss(self) -> None:
@@ -42,12 +44,7 @@ def test_cache_hit_miss(self) -> None:
         # Use string directly instead of Name constructor
         stateful_refs = set()
         cache = Cache(
-            {""var1"": ""value1""},
-            ""hash1"",
-            stateful_refs,
-            ""Pure"",
-            True,
-            {}
+            {""var1"": ""value1""}, ""hash1"", stateful_refs, ""Pure"", True, {}
         )
         loader.save_cache(cache)
 
@@ -66,12 +63,7 @@ def test_load_cache(self) -> None:
         # Use string directly instead of Name constructor
         stateful_refs = set()
         cache = Cache(
-            {""var1"": ""value1""},
-            ""hash1"",
-            stateful_refs,
-            ""Pure"",
-            True,
-            {}
+            {""var1"": ""value1""}, ""hash1"", stateful_refs, ""Pure"", True, {}
         )
         loader.save_cache(cache)
 
@@ -90,27 +82,15 @@ def test_save_cache(self) -> None:
         loader = MemoryLoader(""test"")
 
         # Create and save a cache
-        cache = Cache(
-            {""var1"": ""value1""},
-            ""hash1"",
-            set(),
-            ""Pure"",
-            True,
-            {}
-        )
+        cache = Cache({""var1"": ""value1""}, ""hash1"", set(), ""Pure"", True, {})
         loader.save_cache(cache)
 
         # Verify it was saved
         assert loader.cache_hit(""hash1"", ""Pure"")
 
         # Save another cache with the same hash but different type
         cache2 = Cache(
-            {""var2"": ""value2""},
-            ""hash1"",
-            set(),
-            ""Deferred"",
-            True,
-            {}
+            {""var2"": ""value2""}, ""hash1"", set(), ""Deferred"", True, {}
         )
         loader.save_cache(cache2)
 
@@ -126,12 +106,7 @@ def test_lru_eviction(self) -> None:
         for i in range(3):
             # Use string directly instead of Name constructor
             cache = Cache(
-                {f""var{i}"": f""value{i}""},
-                f""hash{i}"",
-                set(),
-                ""Pure"",
-                True,
-                {}
+                {f""var{i}"": f""value{i}""}, f""hash{i}"", set(), ""Pure"", True, {}
             )
             loader.save_cache(cache)
 
@@ -144,14 +119,7 @@ def test_lru_eviction(self) -> None:
         loader.load_cache(""hash1"", ""Pure"")
 
         # Add another cache
-        cache = Cache(
-            {""var3"": ""value3""},
-            ""hash3"",
-            set(),
-            ""Pure"",
-            True,
-            {}
-        )
+        cache = Cache({""var3"": ""value3""}, ""hash3"", set(), ""Pure"", True, {})
         loader.save_cache(cache)
 
         # hash2 should now be evicted
@@ -168,12 +136,7 @@ def test_resize(self) -> None:
         for i in range(3):
             # Use string directly instead of Name constructor
             cache = Cache(
-                {f""var{i}"": f""value{i}""},
-                f""hash{i}"",
-                set(),
-                ""Pure"",
-                True,
-                {}
+                {f""var{i}"": f""value{i}""}, f""hash{i}"", set(), ""Pure"", True, {}
             )
             loader.save_cache(cache)
 
@@ -201,14 +164,7 @@ def test_resize(self) -> None:
         assert loader.cache_hit(""hash2"", ""Pure"")
 
         # Add a new cache
-        cache = Cache(
-            {""var4"": ""value4""},
-            ""hash4"",
-            set(),
-            ""Pure"",
-            True,
-            {}
-        )
+        cache = Cache({""var4"": ""value4""}, ""hash4"", set(), ""Pure"", True, {})
         loader.save_cache(cache)
 
         # Both should be accessible (no eviction)