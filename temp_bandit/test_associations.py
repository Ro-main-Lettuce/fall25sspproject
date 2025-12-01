@@ -12,7 +12,7 @@
 
 @pytest.fixture
 def source(config):
-    return SourceHubspot()
+    return SourceHubspot(config, None, None)
 
 
 @pytest.fixture