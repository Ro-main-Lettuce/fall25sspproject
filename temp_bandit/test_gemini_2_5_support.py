@@ -1,6 +1,8 @@
 import pytest
+
 from crewai.llm import LLM
 
+
 def test_get_custom_llm_provider_gemini_2_5():
     """"""Test that the Gemini 2.5 model is correctly identified as a Gemini provider.""""""
     llm = LLM(model=""gemini/gemini-2.5-pro-exp-03-25"")