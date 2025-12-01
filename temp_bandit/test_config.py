@@ -21,8 +21,8 @@
 
 def test_requires_app_name():
     """"""Test that a config requires an app_name.""""""
-    with pytest.raises(ValueError):
-        rx.Config()
+    with pytest.raises(TypeError):
+        rx.Config()  # pyright: ignore[reportCallIssue]
 
 
 def test_set_app_name(base_config_values):
@@ -170,7 +170,7 @@ def test_event_namespace(mocker: MockerFixture, kwargs, expected):
         (
             {""backend_port"": 8001, ""frontend_port"": 3001},
             {""REFLEX_BACKEND_PORT"": 8002},
-            {""frontend_port"": ""3005""},
+            {""frontend_port"": 3005},
             {
                 ""api_url"": ""http://localhost:8002"",
                 ""backend_port"": 8002,
@@ -182,7 +182,7 @@ def test_event_namespace(mocker: MockerFixture, kwargs, expected):
         (
             {""api_url"": ""http://foo.bar:8900"", ""deploy_url"": ""http://foo.bar:3001""},
             {""REFLEX_BACKEND_PORT"": 8002},
-            {""frontend_port"": ""3005""},
+            {""frontend_port"": 3005},
             {
                 ""api_url"": ""http://foo.bar:8900"",
                 ""backend_port"": 8002,