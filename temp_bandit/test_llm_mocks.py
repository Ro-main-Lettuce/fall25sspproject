@@ -92,10 +92,10 @@ def mock_openai_api_key():
         yield
 
 @pytest.fixture(autouse=True)
-def mock_gpt_model_validation():
-    """"""Mock GPT model validation to allow mock-model.""""""
-    with patch(""deepeval.models.llms.openai_model.GPTModel._validate_model_name"") as mock_validate:
-        mock_validate.return_value = None  # Do nothing, validation passes
+def mock_model_initialization():
+    """"""Mock model initialization to return our mock model.""""""
+    with patch(""deepeval.metrics.utils.initialize_model"") as mock_initialize:
+        mock_initialize.return_value = (MockLLM(), None)
         yield
 
 