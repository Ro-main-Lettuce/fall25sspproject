@@ -37,9 +37,7 @@ class TestResponse(BaseModel):
 def test_prompt_formatter_create_generic_request():
     """"""Tests that PromptFormatter correctly creates GenericRequest objects.""""""
     # Test with string prompt
-    formatter = PromptFormatter(
-        model_name=""test-model"", prompt_func=lambda x: ""Hello"", response_format=TestResponse
-    )
+    formatter = PromptFormatter(model_name=""test-model"", prompt_func=lambda x: ""Hello"", response_format=TestResponse)
     request = formatter.create_generic_request({""input"": ""test""}, 0)
 
     assert request.model == ""test-model""
@@ -68,12 +66,8 @@ def test_prompt_formatter_invalid_prompt_func():
     """"""Tests that PromptFormatter raises errors for invalid prompt functions.""""""
     # Test prompt function with too many parameters
     with pytest.raises(ValueError, match=""must have 0 or 1 arguments""):
-        PromptFormatter(model_name=""test"", prompt_func=lambda x, y: ""test"").create_generic_request(
-            {}, 0
-        )
+        PromptFormatter(model_name=""test"", prompt_func=lambda x, y: ""test"").create_generic_request({}, 0)
 
     # Test invalid prompt function return type
     with pytest.raises(ValueError, match=""must be a list of dictionaries""):
-        PromptFormatter(
-            model_name=""test"", prompt_func=lambda x: {""invalid"": ""format""}
-        ).create_generic_request({}, 0)
+        PromptFormatter(model_name=""test"", prompt_func=lambda x: {""invalid"": ""format""}).create_generic_request({}, 0)