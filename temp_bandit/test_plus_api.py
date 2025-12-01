@@ -6,43 +6,43 @@
 
 
 class TestPlusAPI(unittest.TestCase):
-    def setUp(self):
+    def setUp(self) -> None:
         self.api_key = ""test_api_key""
         self.api = PlusAPI(self.api_key)
 
-    def test_init(self):
-        self.assertEqual(self.api.api_key, self.api_key)
-        self.assertEqual(self.api.headers[""Authorization""], f""Bearer {self.api_key}"")
-        self.assertEqual(self.api.headers[""Content-Type""], ""application/json"")
-        self.assertTrue(""CrewAI-CLI/"" in self.api.headers[""User-Agent""])
-        self.assertTrue(self.api.headers[""X-Crewai-Version""])
+    def test_init(self) -> None:
+        assert self.api.api_key == self.api_key
+        assert self.api.headers[""Authorization""] == f""Bearer {self.api_key}""
+        assert self.api.headers[""Content-Type""] == ""application/json""
+        assert ""CrewAI-CLI/"" in self.api.headers[""User-Agent""]
+        assert self.api.headers[""X-Crewai-Version""]
 
     @patch(""crewai.cli.plus_api.PlusAPI._make_request"")
-    def test_login_to_tool_repository(self, mock_make_request):
+    def test_login_to_tool_repository(self, mock_make_request) -> None:
         mock_response = MagicMock()
         mock_make_request.return_value = mock_response
 
         response = self.api.login_to_tool_repository()
 
         mock_make_request.assert_called_once_with(
-            ""POST"", ""/crewai_plus/api/v1/tools/login""
+            ""POST"", ""/crewai_plus/api/v1/tools/login"",
         )
-        self.assertEqual(response, mock_response)
+        assert response == mock_response
 
     @patch(""crewai.cli.plus_api.PlusAPI._make_request"")
-    def test_get_tool(self, mock_make_request):
+    def test_get_tool(self, mock_make_request) -> None:
         mock_response = MagicMock()
         mock_make_request.return_value = mock_response
 
         response = self.api.get_tool(""test_tool_handle"")
 
         mock_make_request.assert_called_once_with(
-            ""GET"", ""/crewai_plus/api/v1/tools/test_tool_handle""
+            ""GET"", ""/crewai_plus/api/v1/tools/test_tool_handle"",
         )
-        self.assertEqual(response, mock_response)
+        assert response == mock_response
 
     @patch(""crewai.cli.plus_api.PlusAPI._make_request"")
-    def test_publish_tool(self, mock_make_request):
+    def test_publish_tool(self, mock_make_request) -> None:
         mock_response = MagicMock()
         mock_make_request.return_value = mock_response
         handle = ""test_tool_handle""
@@ -52,7 +52,7 @@ def test_publish_tool(self, mock_make_request):
         encoded_file = ""encoded_test_file""
 
         response = self.api.publish_tool(
-            handle, public, version, description, encoded_file
+            handle, public, version, description, encoded_file,
         )
 
         params = {
@@ -63,12 +63,12 @@ def test_publish_tool(self, mock_make_request):
             ""description"": description,
         }
         mock_make_request.assert_called_once_with(
-            ""POST"", ""/crewai_plus/api/v1/tools"", json=params
+            ""POST"", ""/crewai_plus/api/v1/tools"", json=params,
         )
-        self.assertEqual(response, mock_response)
+        assert response == mock_response
 
     @patch(""crewai.cli.plus_api.PlusAPI._make_request"")
-    def test_publish_tool_without_description(self, mock_make_request):
+    def test_publish_tool_without_description(self, mock_make_request) -> None:
         mock_response = MagicMock()
         mock_make_request.return_value = mock_response
         handle = ""test_tool_handle""
@@ -78,7 +78,7 @@ def test_publish_tool_without_description(self, mock_make_request):
         encoded_file = ""encoded_test_file""
 
         response = self.api.publish_tool(
-            handle, public, version, description, encoded_file
+            handle, public, version, description, encoded_file,
         )
 
         params = {
@@ -89,12 +89,12 @@ def test_publish_tool_without_description(self, mock_make_request):
             ""description"": description,
         }
         mock_make_request.assert_called_once_with(
-            ""POST"", ""/crewai_plus/api/v1/tools"", json=params
+            ""POST"", ""/crewai_plus/api/v1/tools"", json=params,
         )
-        self.assertEqual(response, mock_response)
+        assert response == mock_response
 
     @patch(""crewai.cli.plus_api.requests.Session"")
-    def test_make_request(self, mock_session):
+    def test_make_request(self, mock_session) -> None:
         mock_response = MagicMock()
 
         mock_session_instance = mock_session.return_value
@@ -104,94 +104,91 @@ def test_make_request(self, mock_session):
 
         mock_session.assert_called_once()
         mock_session_instance.request.assert_called_once_with(
-            ""GET"", f""{self.api.base_url}/test_endpoint"", headers=self.api.headers
+            ""GET"", f""{self.api.base_url}/test_endpoint"", headers=self.api.headers,
         )
         mock_session_instance.trust_env = False
-        self.assertEqual(response, mock_response)
+        assert response == mock_response
 
     @patch(""crewai.cli.plus_api.PlusAPI._make_request"")
-    def test_deploy_by_name(self, mock_make_request):
+    def test_deploy_by_name(self, mock_make_request) -> None:
         self.api.deploy_by_name(""test_project"")
         mock_make_request.assert_called_once_with(
-            ""POST"", ""/crewai_plus/api/v1/crews/by-name/test_project/deploy""
+            ""POST"", ""/crewai_plus/api/v1/crews/by-name/test_project/deploy"",
         )
 
     @patch(""crewai.cli.plus_api.PlusAPI._make_request"")
-    def test_deploy_by_uuid(self, mock_make_request):
+    def test_deploy_by_uuid(self, mock_make_request) -> None:
         self.api.deploy_by_uuid(""test_uuid"")
         mock_make_request.assert_called_once_with(
-            ""POST"", ""/crewai_plus/api/v1/crews/test_uuid/deploy""
+            ""POST"", ""/crewai_plus/api/v1/crews/test_uuid/deploy"",
         )
 
     @patch(""crewai.cli.plus_api.PlusAPI._make_request"")
-    def test_crew_status_by_name(self, mock_make_request):
+    def test_crew_status_by_name(self, mock_make_request) -> None:
         self.api.crew_status_by_name(""test_project"")
         mock_make_request.assert_called_once_with(
-            ""GET"", ""/crewai_plus/api/v1/crews/by-name/test_project/status""
+            ""GET"", ""/crewai_plus/api/v1/crews/by-name/test_project/status"",
         )
 
     @patch(""crewai.cli.plus_api.PlusAPI._make_request"")
-    def test_crew_status_by_uuid(self, mock_make_request):
+    def test_crew_status_by_uuid(self, mock_make_request) -> None:
         self.api.crew_status_by_uuid(""test_uuid"")
         mock_make_request.assert_called_once_with(
-            ""GET"", ""/crewai_plus/api/v1/crews/test_uuid/status""
+            ""GET"", ""/crewai_plus/api/v1/crews/test_uuid/status"",
         )
 
     @patch(""crewai.cli.plus_api.PlusAPI._make_request"")
-    def test_crew_by_name(self, mock_make_request):
+    def test_crew_by_name(self, mock_make_request) -> None:
         self.api.crew_by_name(""test_project"")
         mock_make_request.assert_called_once_with(
-            ""GET"", ""/crewai_plus/api/v1/crews/by-name/test_project/logs/deployment""
+            ""GET"", ""/crewai_plus/api/v1/crews/by-name/test_project/logs/deployment"",
         )
 
         self.api.crew_by_name(""test_project"", ""custom_log"")
         mock_make_request.assert_called_with(
-            ""GET"", ""/crewai_plus/api/v1/crews/by-name/test_project/logs/custom_log""
+            ""GET"", ""/crewai_plus/api/v1/crews/by-name/test_project/logs/custom_log"",
         )
 
     @patch(""crewai.cli.plus_api.PlusAPI._make_request"")
-    def test_crew_by_uuid(self, mock_make_request):
+    def test_crew_by_uuid(self, mock_make_request) -> None:
         self.api.crew_by_uuid(""test_uuid"")
         mock_make_request.assert_called_once_with(
-            ""GET"", ""/crewai_plus/api/v1/crews/test_uuid/logs/deployment""
+            ""GET"", ""/crewai_plus/api/v1/crews/test_uuid/logs/deployment"",
         )
 
         self.api.crew_by_uuid(""test_uuid"", ""custom_log"")
         mock_make_request.assert_called_with(
-            ""GET"", ""/crewai_plus/api/v1/crews/test_uuid/logs/custom_log""
+            ""GET"", ""/crewai_plus/api/v1/crews/test_uuid/logs/custom_log"",
         )
 
     @patch(""crewai.cli.plus_api.PlusAPI._make_request"")
-    def test_delete_crew_by_name(self, mock_make_request):
+    def test_delete_crew_by_name(self, mock_make_request) -> None:
         self.api.delete_crew_by_name(""test_project"")
         mock_make_request.assert_called_once_with(
-            ""DELETE"", ""/crewai_plus/api/v1/crews/by-name/test_project""
+            ""DELETE"", ""/crewai_plus/api/v1/crews/by-name/test_project"",
         )
 
     @patch(""crewai.cli.plus_api.PlusAPI._make_request"")
-    def test_delete_crew_by_uuid(self, mock_make_request):
+    def test_delete_crew_by_uuid(self, mock_make_request) -> None:
         self.api.delete_crew_by_uuid(""test_uuid"")
         mock_make_request.assert_called_once_with(
-            ""DELETE"", ""/crewai_plus/api/v1/crews/test_uuid""
+            ""DELETE"", ""/crewai_plus/api/v1/crews/test_uuid"",
         )
 
     @patch(""crewai.cli.plus_api.PlusAPI._make_request"")
-    def test_list_crews(self, mock_make_request):
+    def test_list_crews(self, mock_make_request) -> None:
         self.api.list_crews()
         mock_make_request.assert_called_once_with(""GET"", ""/crewai_plus/api/v1/crews"")
 
     @patch(""crewai.cli.plus_api.PlusAPI._make_request"")
-    def test_create_crew(self, mock_make_request):
+    def test_create_crew(self, mock_make_request) -> None:
         payload = {""name"": ""test_crew""}
         self.api.create_crew(payload)
         mock_make_request.assert_called_once_with(
-            ""POST"", ""/crewai_plus/api/v1/crews"", json=payload
+            ""POST"", ""/crewai_plus/api/v1/crews"", json=payload,
         )
 
     @patch.dict(os.environ, {""CREWAI_BASE_URL"": ""https://custom-url.com/api""})
-    def test_custom_base_url(self):
+    def test_custom_base_url(self) -> None:
         custom_api = PlusAPI(""test_key"")
-        self.assertEqual(
-            custom_api.base_url,
-            ""https://custom-url.com/api"",
-        )
+        assert custom_api.base_url == ""https://custom-url.com/api""