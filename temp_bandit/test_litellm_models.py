@@ -2,10 +2,9 @@
 import os
 
 import pytest
-from datasets import Dataset
 
 from bespokelabs.curator import LLM
-from tests.helpers import clear_test_cache
+from bespokelabs.curator.dataset import Dataset
 
 """"""
 USAGE:
@@ -16,8 +15,20 @@
 @pytest.mark.cache_dir(os.path.expanduser(""~/.cache/curator-tests/test-models""))
 @pytest.mark.usefixtures(""clear_test_cache"")
 class TestLiteLLMModels:
+    """"""Test suite for validating various LLM models through the LiteLLM backend.
+
+    This test class verifies that different language models can be accessed and used
+    through curator's LLM interface using the LiteLLM backend. It tests a variety of
+    models from different providers including Anthropic, OpenAI, Google, and Together.ai.
+    """"""
+
     @pytest.fixture(autouse=True)
     def check_environment(self):
+        """"""Fixture to verify required API keys are present in environment variables.
+
+        Raises:
+            AssertionError: If any required API key is missing from environment variables.
+        """"""
         env = os.environ.copy()
         required_keys = [
             ""ANTHROPIC_API_KEY"",
@@ -43,12 +54,18 @@ def check_environment(self):
             pytest.param(""gemini/gemini-1.5-flash"", id=""gemini-flash""),
             pytest.param(""gemini/gemini-1.5-pro"", id=""gemini-pro""),
             pytest.param(""together_ai/meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"", id=""llama-8b""),
-            pytest.param(
-                ""together_ai/meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo"", id=""llama-70b""
-            ),
+            pytest.param(""together_ai/meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo"", id=""llama-70b""),
         ],
     )
     def test_model(self, model):
+        """"""Test a specific LLM model's basic functionality.
+
+        Tests that the model can successfully process a simple prompt and return a response
+        through the curator LLM interface using LiteLLM backend.
+
+        Args:
+            model (str): The identifier/name of the model to test.
+        """"""
         print(f""

========== TESTING {model} ==========

"")
         logger = logging.getLogger(""bespokelabs.curator"")
         logger.setLevel(logging.DEBUG)