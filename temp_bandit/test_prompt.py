@@ -1,6 +1,6 @@
 import os
 from typing import Optional
-from unittest.mock import MagicMock, patch
+from unittest.mock import patch
 
 import pytest
 from datasets import Dataset
@@ -62,9 +62,7 @@ def test_completions(prompter: LLM, tmp_path):
     os.environ[""BELLA_CACHE_DIR""] = str(tmp_path)
 
     # Mock OpenAI API response
-    mock_response = {
-        ""choices"": [{""message"": {""content"": ""1 + 1 equals 2.""}, ""finish_reason"": ""stop""}]
-    }
+    mock_response = {""choices"": [{""message"": {""content"": ""1 + 1 equals 2.""}, ""finish_reason"": ""stop""}]}
 
     with patch(""openai.resources.chat.completions.Completions.create"", return_value=mock_response):
         # Process dataset and get responses
@@ -113,9 +111,7 @@ def simple_prompt_func():
     )
 
     # Mock response data
-    mock_dataset = Dataset.from_list(
-        [{""response"": {""message"": ""This is a test message."", ""confidence"": 0.9}}]
-    )
+    mock_dataset = Dataset.from_list([{""response"": {""message"": ""This is a test message."", ""confidence"": 0.9}}])
 
     # Mock the run method of OpenAIBatchRequestProcessor
     with patch(
@@ -161,9 +157,7 @@ def simple_prompt_func():
     )
 
     # Mock response data
-    mock_dataset = Dataset.from_list(
-        [{""response"": {""message"": ""This is a test message."", ""confidence"": 0.9}}]
-    )
+    mock_dataset = Dataset.from_list([{""response"": {""message"": ""This is a test message."", ""confidence"": 0.9}}])
 
     # Mock the run method of OpenAIOnlineRequestProcessor
     with patch(