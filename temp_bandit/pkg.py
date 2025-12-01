@@ -17,6 +17,8 @@
     ""get_pkg_version"",
     ""source_locations"",
     ""find_spec"",
+    ""find_uv"",
+    ""ensure_uv"",
 ]
 
 get_pkg_version = importlib.metadata.version
@@ -43,6 +45,48 @@ def source_locations(pkg: str) -> str | None:
 
 
 @lru_cache(maxsize=1)
+def find_uv() -> str | None:
+    """"""Find uv executable in PATH.""""""
+    import shutil
+
+    return shutil.which(""uv"")
+
+
+def ensure_uv() -> str:
+    """"""Ensure uv is available, installing if needed.
+
+    Returns:
+        str: The name of the uv executable (""uv"")
+
+    Raises:
+        BentoMLException: If uv is not found and cannot be installed
+    """"""
+    if find_uv():
+        return ""uv""
+
+    import logging
+    import subprocess
+    import sys
+
+    from bentoml.exceptions import BentoMLException
+
+    logger = logging.getLogger(__name__)
+    logger.info(""uv not found, attempting to install..."")
+    try:
+        subprocess.check_call(
+            [sys.executable, ""-m"", ""pip"", ""install"", ""--quiet"", ""uv>=0.5""],
+            stderr=subprocess.PIPE,
+        )
+        if find_uv():
+            return ""uv""
+    except subprocess.CalledProcessError:
+        pass
+
+    raise BentoMLException(
+        ""'uv' not found and automatic installation failed. Please install uv manually: pip install uv>=0.5""
+    )
+
+
 def get_local_bentoml_dependency() -> str:
     import logging
 