@@ -269,7 +269,7 @@ def draw(self, _context: Context) -> None:
             ""The current file is not compatible with the running Blender.
""
             + ""The current file was created in Blender {file_version}, but the running""
             + "" Blender version is {app_version}.
""
-            + ""So it is not compatible. As a result some data may be lost or corrupted.""
+            + ""This incompatibility may result in data loss or corruption.""
         ).format(
             app_version=self.app_version,
             file_version=self.file_version,
@@ -316,9 +316,8 @@ def draw(self, _context: Context) -> None:
             ""The current file is not compatible with the installed VRM Add-on.
""
             + ""The current file was created in VRM Add-on {file_addon_version}, but the""
             + "" installed
""
-            + ""VRM Add-on version is {installed_addon_version}. So it is not""
-            + "" compatible. As a result some
""
-            + ""data may be lost or corrupted.""
+            + ""VRM Add-on version is {installed_addon_version}. This incompatibility
""
+            + ""may result in data loss or corruption.""
         ).format(
             file_addon_version=self.file_addon_version,
             installed_addon_version=self.installed_addon_version,