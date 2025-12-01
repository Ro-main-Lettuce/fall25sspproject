@@ -14,7 +14,7 @@ class Bun(SimpleNamespace):
     """"""Bun constants.""""""
 
     # The Bun version.
-    VERSION = ""1.2.17""
+    VERSION = ""1.2.18""
 
     # Min Bun Version
     MIN_VERSION = ""1.2.17""
@@ -143,10 +143,11 @@ def DEPENDENCIES(cls) -> dict[str, str]:
         ""postcss-import"": ""16.1.1"",
         ""@react-router/dev"": _react_router_version,
         ""@react-router/fs-routes"": _react_router_version,
-        ""rolldown-vite"": ""7.0.5"",
+        ""rolldown-vite"": ""7.0.8"",
     }
     OVERRIDES = {
         # This should always match the `react` version in DEPENDENCIES for recharts compatibility.
         ""react-is"": _react_version,
         ""cookie"": ""1.0.2"",
+        ""rollup"": ""4.44.2"",
     }