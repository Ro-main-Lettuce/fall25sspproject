@@ -4,9 +4,9 @@
 from unittest import TestCase
 from unittest.mock import patch
 
+from airbyte_cdk.models import Level as LogLevel
+from airbyte_cdk.models import SyncMode
 from airbyte_cdk.test.mock_http import HttpMocker
-from airbyte_protocol.models import Level as LogLevel
-from airbyte_protocol.models import SyncMode
 
 from .config import ConfigBuilder
 from .monday_requests import TeamsRequestBuilder
@@ -49,6 +49,7 @@ def test_given_retryable_error_and_one_page_when_read_teams_then_return_records(
             (""200_complexityBudgetExhausted"", ""complexityBudgetExhausted""),
         ]
         for test_values in test_cases:
+            http_mocker.clear_all_matchers()
             response, error_code = test_values[0], test_values[1]
             api_token_authenticator = self.get_authenticator(self._config)
 
@@ -68,7 +69,7 @@ def test_given_retryable_error_and_one_page_when_read_teams_then_return_records(
             error_logs = [
                 error
                 for error in get_log_messages_by_log_level(output.logs, LogLevel.INFO)
-                if f'Response Code: 200, Response Text: {json.dumps({""error_code"": error_code, ""status_code"": 200})}' in error
+                if f'Status code: 200, Response Content: b\'{json.dumps({""error_code"": error_code, ""status_code"": 200})}\'' in error
             ]
             assert len(error_logs) == 1
 
@@ -91,9 +92,9 @@ def test_given_retryable_error_when_read_teams_then_stop_syncing(self, http_mock
         error_logs = [
             error
             for error in get_log_messages_by_log_level(output.logs, LogLevel.INFO)
-            if f'Response Code: 200, Response Text: {json.dumps({""error_code"": ""ComplexityException"", ""status_code"": 200})}' in error
+            if f'Status code: 200, Response Content: b\'{json.dumps({""error_code"": ""ComplexityException"", ""status_code"": 200})}\'' in error
         ]
-        assert len(error_logs) == 6
+        assert len(error_logs) == 5
 
     @HttpMocker()
     def test_given_retryable_500_error_when_read_teams_then_stop_syncing(self, http_mocker):
@@ -114,9 +115,10 @@ def test_given_retryable_500_error_when_read_teams_then_stop_syncing(self, http_
         error_logs = [
             error
             for error in get_log_messages_by_log_level(output.logs, LogLevel.INFO)
-            if f'Response Code: 500, Response Text: {json.dumps({""error_message"": ""Internal server error"", ""status_code"": 500})}' in error
+            if ""Backing off _send(...) for 0.0s (airbyte_cdk.sources.streams.http.exceptions.UserDefinedBackoffException: Internal server error.""
+            in error
         ]
-        assert len(error_logs) == 6
+        assert len(error_logs) == 5
 
     @HttpMocker()
     def test_given_403_error_when_read_teams_then_ignore_the_stream(self, http_mocker):
@@ -134,9 +136,5 @@ def test_given_403_error_when_read_teams_then_ignore_the_stream(self, http_mocke
 
         assert len(output.records) == 0
 
-        error_logs = [
-            error
-            for error in get_log_messages_by_log_level(output.logs, LogLevel.INFO)
-            if ""Ignoring response for failed request with error message None"" in error
-        ]
-        assert len(error_logs) == 1
+        # Ignored error with no access to the requested entity
+        assert len(output.errors) == 0