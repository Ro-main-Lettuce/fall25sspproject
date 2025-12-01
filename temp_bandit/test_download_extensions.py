@@ -1,6 +1,7 @@
 from __future__ import annotations
 
 import os
+import platform
 import shutil
 import tarfile
 from typing import TYPE_CHECKING
@@ -58,7 +59,18 @@ def test_remote_extensions(
     extensions_endpoint = f""http://{host}:{port}/pg-ext-s3-gateway""
 
     build_tag = os.environ.get(""BUILD_TAG"", ""latest"")
-    archive_route = f""{build_tag}/v{pg_version}/extensions/test_extension.tar.zst""
+
+    # We have decided to use the Go naming convention due to Kubernetes.
+    arch = platform.machine()
+    match arch:
+        case ""aarch64"":
+            arch = ""arm64""
+        case ""x86_64"":
+            arch = ""amd64""
+        case _:
+            pass
+
+    archive_route = f""{build_tag}/{arch}/v{pg_version}/extensions/test_extension.tar.zst""
     tarball = test_output_dir / ""test_extension.tar""
     extension_dir = (
         base_dir / ""test_runner"" / ""regress"" / ""data"" / ""test_remote_extensions"" / ""test_extension""