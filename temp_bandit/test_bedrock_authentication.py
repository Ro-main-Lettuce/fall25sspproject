@@ -1,4 +1,5 @@
 import os
+import pytest
 from unittest.mock import patch, MagicMock
 from crewai import LLM
 
@@ -106,3 +107,71 @@ def test_bedrock_api_key_different_region(self, mock_completion):
         
         mock_completion.assert_called_once()
         assert result == ""Test response""
+    @patch.dict(os.environ, {
+        'AWS_BEARER_TOKEN_BEDROCK': 'test-api-key',
+        'AWS_DEFAULT_REGION': 'us-east-1'
+    })
+    @patch('litellm.completion')
+    def test_bedrock_timeout_handling(self, mock_completion):
+        """"""Test Bedrock API timeout handling.""""""
+        mock_completion.side_effect = TimeoutError(""Request timed out"")
+        
+        llm = LLM(model=""bedrock/anthropic.claude-3-sonnet-20240229-v1:0"")
+        with pytest.raises(TimeoutError, match=""Request timed out""):
+            llm.call(""test message"")
+
+    @patch.dict(os.environ, {
+        'AWS_BEARER_TOKEN_BEDROCK': 'test-api-key',
+        'AWS_DEFAULT_REGION': 'us-east-1'
+    })
+    @patch('litellm.completion')
+    def test_bedrock_rate_limit_handling(self, mock_completion):
+        """"""Test Bedrock API rate limit handling.""""""
+        mock_completion.side_effect = Exception(""Rate limit exceeded"")
+        
+        llm = LLM(model=""bedrock/anthropic.claude-3-sonnet-20240229-v1:0"")
+        with pytest.raises(Exception, match=""Rate limit exceeded""):
+            llm.call(""test message"")
+
+    @patch.dict(os.environ, {
+        'AWS_BEARER_TOKEN_BEDROCK': 'invalid-key',
+        'AWS_DEFAULT_REGION': 'us-east-1'
+    })
+    @patch('litellm.completion')
+    def test_bedrock_invalid_api_key(self, mock_completion):
+        """"""Test Bedrock with invalid API key.""""""
+        mock_completion.side_effect = Exception(""Invalid API key"")
+        
+        llm = LLM(model=""bedrock/anthropic.claude-3-sonnet-20240229-v1:0"")
+        with pytest.raises(Exception, match=""Invalid API key""):
+            llm.call(""test message"")
+
+    @patch.dict(os.environ, {
+        'AWS_ACCESS_KEY_ID': 'test-key-id',
+        'AWS_SECRET_ACCESS_KEY': 'test-secret-key',
+        'AWS_DEFAULT_REGION': 'us-east-1'
+    })
+    @patch('litellm.completion')
+    def test_bedrock_connection_error(self, mock_completion):
+        """"""Test Bedrock with connection error.""""""
+        mock_completion.side_effect = ConnectionError(""Connection failed"")
+        
+        llm = LLM(model=""bedrock/anthropic.claude-3-sonnet-20240229-v1:0"")
+        with pytest.raises(ConnectionError, match=""Connection failed""):
+            llm.call(""test message"")
+
+    @patch.dict(os.environ, {
+        'AWS_BEARER_TOKEN_BEDROCK': 'test-api-key',
+        'AWS_DEFAULT_REGION': 'us-east-1'
+    })
+    @patch('litellm.completion')
+    def test_bedrock_api_key_with_retry_scenario(self, mock_completion):
+        """"""Test Bedrock API key authentication with retry scenario.""""""
+        mock_completion.side_effect = [
+            Exception(""Temporary error""),
+            MagicMock(choices=[MagicMock(message=MagicMock(content=""Success after retry""))])
+        ]
+        
+        llm = LLM(model=""bedrock/anthropic.claude-3-sonnet-20240229-v1:0"")
+        with pytest.raises(Exception, match=""Temporary error""):
+            llm.call(""test message"")