@@ -1,5 +1,3 @@
-import pytest
-
 from crewai.cli.constants import ENV_VARS, JSON_URL, MODELS, PROVIDERS
 
 
@@ -26,4 +24,4 @@ def test_huggingface_models():
 def test_json_url_is_https():
     """"""Test that JSON_URL uses HTTPS for secure connection.""""""
     assert JSON_URL.startswith(""https://"")
-    assert ""raw.githubusercontent.com"" in JSON_URL
+    assert JSON_URL == ""https://raw.githubusercontent.com/BerriAI/litellm/main/model_prices_and_context_window.json""