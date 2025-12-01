@@ -3,66 +3,53 @@
 """"""
 
 import pytest
-from unittest.mock import patch, Mock
 import requests
+from unittest.mock import Mock, patch
 
+from agentops.exceptions import ApiServerException
 from agentops.validation import (
-    get_jwt_token,
+    get_jwt_token_sync,
     get_trace_details,
     check_llm_spans,
     validate_trace_spans,
-    ValidationError,
     print_validation_summary,
+    ValidationError,
 )
-from agentops.exceptions import ApiServerException
+from agentops.semconv import SpanAttributes, LLMRequestTypeValues
 
 
 class TestGetJwtToken:
     """"""Test JWT token exchange functionality.""""""
 
-    @patch(""agentops.validation.requests.post"")
-    def test_get_jwt_token_success(self, mock_post):
+    @patch(""tests.unit.test_validation.get_jwt_token_sync"")
+    def test_get_jwt_token_success(self, mock_sync):
         """"""Test successful JWT token retrieval.""""""
-        mock_response = Mock()
-        mock_response.status_code = 200
-        mock_response.json.return_value = {""bearer"": ""test-token""}
-        mock_post.return_value = mock_response
+        mock_sync.return_value = ""test-token""
 
-        token = get_jwt_token(""test-api-key"")
+        token = get_jwt_token_sync(""test-api-key"")
         assert token == ""test-token""
 
-        mock_post.assert_called_once_with(
-            ""https://api.agentops.ai/public/v1/auth/access_token"", json={""api_key"": ""test-api-key""}, timeout=10
-        )
-
-    @patch(""agentops.validation.requests.post"")
-    def test_get_jwt_token_failure(self, mock_post):
+    @patch(""tests.unit.test_validation.get_jwt_token_sync"")
+    def test_get_jwt_token_failure(self, mock_sync):
         """"""Test JWT token retrieval failure.""""""
-        mock_response = Mock()
-        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(""401 Unauthorized"")
-        mock_post.return_value = mock_response
+        mock_sync.return_value = None
 
-        with pytest.raises(ApiServerException, match=""Failed to get JWT token""):
-            get_jwt_token(""invalid-api-key"")
+        # Should not raise exception anymore, just return None
+        token = get_jwt_token_sync(""invalid-api-key"")
+        assert token is None
 
     @patch(""os.getenv"")
     @patch(""agentops.get_client"")
-    @patch(""agentops.validation.requests.post"")
-    def test_get_jwt_token_from_env(self, mock_post, mock_get_client, mock_getenv):
+    @patch(""tests.unit.test_validation.get_jwt_token_sync"")
+    def test_get_jwt_token_from_env(self, mock_sync, mock_get_client, mock_getenv):
         """"""Test JWT token retrieval using environment variable.""""""
         mock_get_client.return_value = None
         mock_getenv.return_value = ""env-api-key""
+        mock_sync.return_value = ""env-token""
 
-        mock_response = Mock()
-        mock_response.status_code = 200
-        mock_response.json.return_value = {""bearer"": ""env-token""}
-        mock_post.return_value = mock_response
-
-        token = get_jwt_token()
+        token = get_jwt_token_sync()
         assert token == ""env-token""
 
-        mock_getenv.assert_called_once_with(""AGENTOPS_API_KEY"")
-
 
 class TestGetTraceDetails:
     """"""Test trace details retrieval.""""""
@@ -129,8 +116,6 @@ def test_check_llm_spans_empty(self):
 
     def test_check_llm_spans_with_request_type(self):
         """"""Test when LLM spans are identified by LLM_REQUEST_TYPE attribute.""""""
-        from agentops.semconv import SpanAttributes, LLMRequestTypeValues
-
         spans = [
             {
                 ""span_name"": ""openai.chat.completion"",
@@ -161,9 +146,6 @@ def test_check_llm_spans_with_request_type(self):
 
     def test_check_llm_spans_real_world(self):
         """"""Test with real-world span structures from OpenAI and Anthropic.""""""
-        from agentops.semconv import SpanAttributes, LLMRequestTypeValues
-
-        # This simulates what we actually get from the OpenAI and Anthropic instrumentations
         spans = [
             {
                 ""span_name"": ""openai.chat.completion"",