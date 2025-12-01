@@ -20,7 +20,7 @@ def dummy_version(self):
 
     def test_class_attributes(self):
         """"""Spot any regression in the class attributes.""""""
-        assert bases.AirbytePythonConnectorBaseImage.root_image == root_images.PYTHON_3_11_11
+        assert bases.AirbytePythonConnectorBaseImage.root_image == root_images.PYTHON_3_11_13
         assert bases.AirbytePythonConnectorBaseImage.repository == ""airbyte/python-connector-base""
         assert bases.AirbytePythonConnectorBaseImage.pip_cache_name == ""pip_cache""
 