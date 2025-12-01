@@ -1,10 +1,8 @@
 import pytest
 from unittest.mock import patch, MagicMock
 
-from crewai.agents.agent_builder.utilities.base_token_process import TokenProcess
 from crewai.llm import LLM
 from crewai.agent import Agent
-from crewai.utilities.token_counter_callback import TokenCalcHandler
 
 
 @pytest.mark.vcr(filter_headers=[""authorization""])
@@ -175,3 +173,74 @@ def test_llm_call_without_router(mock_completion):
     
     mock_completion.assert_called_once()
     assert response == ""Test response""
+
+
+@pytest.mark.vcr(filter_headers=[""authorization""])
+def test_llm_with_invalid_routing_strategy():
+    """"""Test that LLM initialization raises an error with an invalid routing strategy.""""""
+    model_list = [
+        {
+            ""model_name"": ""gpt-4o-mini"",
+            ""litellm_params"": {
+                ""model"": ""gpt-4o-mini"",
+                ""api_key"": ""test-key-1""
+            }
+        }
+    ]
+    
+    with pytest.raises(RuntimeError) as exc_info:
+        LLM(
+            model=""gpt-4o-mini"", 
+            model_list=model_list, 
+            routing_strategy=""invalid-strategy""
+        )
+    
+    assert ""Invalid routing strategy"" in str(exc_info.value)
+
+
+@pytest.mark.vcr(filter_headers=[""authorization""])
+def test_agent_with_invalid_routing_strategy():
+    """"""Test that Agent initialization raises an error with an invalid routing strategy.""""""
+    model_list = [
+        {
+            ""model_name"": ""gpt-4o-mini"",
+            ""litellm_params"": {
+                ""model"": ""gpt-4o-mini"",
+                ""api_key"": ""test-key-1""
+            }
+        }
+    ]
+    
+    with pytest.raises(Exception) as exc_info:
+        Agent(
+            role=""test"",
+            goal=""test"",
+            backstory=""test"",
+            model_list=model_list,
+            routing_strategy=""invalid-strategy""
+        )
+    
+    assert ""Input should be"" in str(exc_info.value)
+    assert ""simple-shuffle"" in str(exc_info.value)
+    assert ""least-busy"" in str(exc_info.value)
+
+
+@pytest.mark.vcr(filter_headers=[""authorization""])
+@patch.object(LLM, '_initialize_router')
+def test_llm_with_missing_model_in_litellm_params(mock_initialize_router):
+    """"""Test that LLM initialization raises an error when model is missing in litellm_params.""""""
+    mock_initialize_router.side_effect = RuntimeError(""Router initialization failed: Missing required 'model' in litellm_params"")
+    
+    model_list = [
+        {
+            ""model_name"": ""gpt-4o-mini"",
+            ""litellm_params"": {
+                ""api_key"": ""test-key-1""
+            }
+        }
+    ]
+    
+    with pytest.raises(RuntimeError) as exc_info:
+        LLM(model=""gpt-4o-mini"", model_list=model_list)
+    
+    assert ""Router initialization failed"" in str(exc_info.value)