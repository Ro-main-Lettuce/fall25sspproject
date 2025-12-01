@@ -64,7 +64,7 @@ class ManifestOnlyConnectorUnitTests(PytestStep):
 
     title = ""Manifest-only unit tests""
     test_directory_name = ""unit_tests""
-    common_test_dependencies = [""pytest""]
+    common_test_dependencies = [""pytest"", ""requests-mock""]
 
     async def install_testing_environment(
         self,