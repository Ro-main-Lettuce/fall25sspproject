@@ -63,7 +63,7 @@ def mock_risk_assessment():
 
 
 class TestRedTeam:
-    @patch(""deepteam.red_team.RedTeamer"")
+    @patch(""deepteam.red_team.RedTeamer"", autospec=True)
     def test_red_team_function(self, mock_red_teamer_class, mock_sync_callback, mock_vulnerability, mock_attack):
         mock_red_teamer = mock_red_teamer_class.return_value
         mock_red_teamer.red_team.return_value = ""mock_risk_assessment""
@@ -90,7 +90,7 @@ def test_red_team_function(self, mock_red_teamer_class, mock_sync_callback, mock
         
         assert result == ""mock_risk_assessment""
 
-    @patch(""deepteam.red_team.RedTeamer"")
+    @patch(""deepteam.red_team.RedTeamer"", autospec=True)
     def test_red_team_function_async(self, mock_red_teamer_class, mock_async_callback, mock_vulnerability, mock_attack):
         mock_red_teamer = mock_red_teamer_class.return_value
         mock_red_teamer.red_team.return_value = ""mock_risk_assessment""