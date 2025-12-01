@@ -621,8 +621,11 @@ def test_handle_streaming_tool_calls_no_tools(mock_emit):
 
 
 def test_llama_api_support():
-    """"""Test that Llama API models are correctly configured.""""""
-    from crewai.cli.constants import MODELS, PROVIDERS, ENV_VARS, LITELLM_PARAMS
+    """"""
+    Test Llama API configuration and integration.
+    - Verifies provider registration, model availability, environment variables, and context window sizes.
+    """"""
+    from crewai.cli.constants import ENV_VARS, LITELLM_PARAMS, MODELS, PROVIDERS
     from crewai.llm import LLM_CONTEXT_WINDOW_SIZES
     
     assert ""meta-llama"" in PROVIDERS