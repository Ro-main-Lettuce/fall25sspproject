@@ -10,7 +10,7 @@
 from base_images import bases, published_image
 from base_images import sanity_checks as base_sanity_checks
 from base_images.python import sanity_checks as python_sanity_checks
-from base_images.root_images import PYTHON_3_11_11
+from base_images.root_images import PYTHON_3_11_13
 
 
 class AirbyteManifestOnlyConnectorBaseImage(bases.AirbyteConnectorBaseImage):
@@ -20,7 +20,7 @@ class AirbyteManifestOnlyConnectorBaseImage(bases.AirbyteConnectorBaseImage):
 
 
 class AirbytePythonConnectorBaseImage(bases.AirbyteConnectorBaseImage):
-    root_image: Final[published_image.PublishedImage] = PYTHON_3_11_11
+    root_image: Final[published_image.PublishedImage] = PYTHON_3_11_13
     repository: Final[str] = ""airbyte/python-connector-base""
     pip_cache_name: Final[str] = ""pip_cache""
     nltk_data_path: Final[str] = ""/usr/share/nltk_data""
@@ -63,7 +63,7 @@ def with_tesseract_and_poppler(container: dagger.Container) -> dagger.Container:
             """"""
 
             container = container.with_exec(
-                [""sh"", ""-c"", ""apt-get update && apt-get install -y tesseract-ocr=5.3.0-2 poppler-utils=22.12.0-2+b1""]
+                [""sh"", ""-c"", ""apt-get update && apt-get install -y tesseract-ocr=5.3.0-2 poppler-utils=22.12.0-2+deb12u1""]
             )
 
             return container
@@ -125,7 +125,7 @@ async def run_sanity_checks(self, platform: dagger.Platform):
         container = self.get_container(platform)
         await base_sanity_checks.check_timezone_is_utc(container)
         await base_sanity_checks.check_a_command_is_available_using_version_option(container, ""bash"")
-        await python_sanity_checks.check_python_version(container, ""3.11.11"")
+        await python_sanity_checks.check_python_version(container, ""3.11.13"")
         await python_sanity_checks.check_pip_version(container, ""24.0"")
         await base_sanity_checks.check_user_exists(container, self.USER, expected_uid=self.USER_ID, expected_gid=self.USER_ID)
         await base_sanity_checks.check_user_can_read_dir(container, self.USER, self.AIRBYTE_DIR_PATH)