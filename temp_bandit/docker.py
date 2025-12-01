@@ -42,9 +42,9 @@ def ensure_installation(
         """"""
         _ = auto_fix
         try:
-            assert shutil.which(""docker"") is not None, (
-                ""Docker couldn't be found on your system. Please Install it.""
-            )
+            assert (
+                shutil.which(""docker"") is not None
+            ), ""Docker couldn't be found on your system. Please Install it.""
             self.execute([""spec""])
         except Exception as e:
             raise exc.AirbyteConnectorExecutableNotFoundError(