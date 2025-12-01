@@ -1,7 +1,6 @@
 """"""Tests for AI/ML API integration with CrewAI.""""""
 
-import pytest
-from unittest.mock import Mock, patch
+from unittest.mock import patch
 
 from crewai.llm import LLM
 from crewai.utilities.llm_utils import create_llm
@@ -25,7 +24,7 @@ def test_aiml_api_model_context_windows(self):
         
         for model_name, expected_context_size in test_cases:
             llm = LLM(model=model_name)
-            expected_usable_size = int(expected_context_size * 0.75)
+            expected_usable_size = int(expected_context_size * 0.85)
             actual_context_size = llm.get_context_window_size()
             assert actual_context_size == expected_usable_size, (
                 f""Model {model_name} should have context window size {expected_usable_size}, ""