@@ -177,12 +177,12 @@ def test_list_crews(self):
     def test_get_crew_status(self):
         mock_response = MagicMock()
         mock_response.status_code = 200
-        mock_response.json.return_value = {""name"": ""TestCrew"", ""status"": ""active""}
+        mock_response.json.return_value = {""name"": ""InternalCrew"", ""status"": ""active""}
         self.mock_client.crew_status_by_name.return_value = mock_response
 
         with patch(""sys.stdout"", new=StringIO()) as fake_out:
             self.deploy_command.get_crew_status()
-            self.assertIn(""TestCrew"", fake_out.getvalue())
+            self.assertIn(""InternalCrew"", fake_out.getvalue())
             self.assertIn(""active"", fake_out.getvalue())
 
     def test_get_crew_logs(self):