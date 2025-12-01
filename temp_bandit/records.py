@@ -148,8 +148,11 @@ def __init__(
         }
 
     def to_display_case(self, key: str) -> str:
-        """"""Return the original case of the key.""""""
-        return self._pretty_case_lookup[self._normalizer.normalize(key)]
+        """"""Return the original case of the key.
+
+        If the key is not found in the pretty case lookup, return the key provided.
+        """"""
+        return self._pretty_case_lookup.get(self._normalizer.normalize(key), key)
 
     def to_index_case(self, key: str) -> str:
         """"""Return the internal case of the key.