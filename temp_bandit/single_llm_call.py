@@ -77,44 +77,63 @@ async def run(self, input_data: BaseModel) -> BaseModel:
 
 
 if __name__ == ""__main__"":
+    import asyncio
+    import os
 
     async def test_llm_nodes():
-        # Example 1: Simple test case with a basic user message
-        simple_llm_node = SingleLLMCallNode(
-            config=SingleLLMCallNodeConfig(
-                llm_info=ModelInfo(
-                    model=LLMModels.GPT_4O_MINI, temperature=0.1, max_tokens=100
-                ),
-                system_message=""This is a simple test prompt for {{ your_name }}."",
-                user_message=""Hello, my name is {{ your_name }}. I want to ask: {{ user_message }}"",
-                output_schema={""response"": ""str"", ""your_name"": ""str""},
-                input_schema={""user_message"": ""str"", ""your_name"": ""str""},
+        # Save original env var if it exists
+        original_base_url = os.getenv(""OPENAI_BASE_URL"")
+        
+        try:
+            # Test with base URL unset
+            if ""OPENAI_BASE_URL"" in os.environ:
+                del os.environ[""OPENAI_BASE_URL""]
+            
+            # Example 1: Simple test case with a basic user message
+            simple_llm_node = SingleLLMCallNode(
+                config=SingleLLMCallNodeConfig(
+                    llm_info=ModelInfo(
+                        model=LLMModels.GPT_4O_MINI, temperature=0.1, max_tokens=100
+                    ),
+                    system_message=""This is a simple test prompt for {{ your_name }}."",
+                    user_message=""Hello, my name is {{ your_name }}. I want to ask: {{ user_message }}"",
+                    output_schema={""response"": ""str"", ""your_name"": ""str""},
+                    input_schema={""user_message"": ""str"", ""your_name"": ""str""},
+                )
             )
-        )
-        simple_input = simple_llm_node.input_model.model_validate(
-            {""user_message"": ""What is the weather today?"", ""your_name"": ""Alice""}
-        )
-        simple_output = await simple_llm_node(simple_input)
-        print(""Simple Test Output:"", simple_output)
-
-        # Example 2: More complex test case with additional variables
-        complex_llm_node = SingleLLMCallNode(
-            config=SingleLLMCallNodeConfig(
-                llm_info=ModelInfo(
-                    model=LLMModels.GPT_4O_MINI, temperature=0.2, max_tokens=200
-                ),
-                system_message=""This is a complex test prompt for {{ your_name }}, who is {{ age }} years old."",
-                user_message=""Hi, I am {{ your_name }}. I am {{ age }} years old and I want to ask: {{ user_message }}"",
-                output_schema={""response"": ""str"", ""your_name"": ""str"", ""age"": ""int""},
-                input_schema={""user_message"": ""str"", ""your_name"": ""str"", ""age"": ""int""},
+            simple_input = simple_llm_node.input_model.model_validate(
+                {""user_message"": ""What is the weather today?"", ""your_name"": ""Alice""}
             )
-        )
-        complex_input = complex_llm_node.input_model.model_validate(
-            {""user_message"": ""Can you tell me a joke?"", ""your_name"": ""Bob"", ""age"": 30}
-        )
-        complex_output = await complex_llm_node(complex_input)
-        print(""Complex Test Output:"", complex_output)
-
-    import asyncio
+            simple_output = await simple_llm_node(simple_input)
+            print(""Simple Test Output:"", simple_output)
+
+            # Example 2: More complex test case with additional variables
+            complex_llm_node = SingleLLMCallNode(
+                config=SingleLLMCallNodeConfig(
+                    llm_info=ModelInfo(
+                        model=LLMModels.GPT_4O_MINI, temperature=0.2, max_tokens=200
+                    ),
+                    system_message=""This is a complex test prompt for {{ your_name }}, who is {{ age }} years old."",
+                    user_message=""Hi, I am {{ your_name }}. I am {{ age }} years old and I want to ask: {{ user_message }}"",
+                    output_schema={""response"": ""str"", ""your_name"": ""str"", ""age"": ""int""},
+                    input_schema={""user_message"": ""str"", ""your_name"": ""str"", ""age"": ""int""},
+                )
+            )
+            complex_input = complex_llm_node.input_model.model_validate(
+                {""user_message"": ""Can you tell me a joke?"", ""your_name"": ""Bob"", ""age"": 30}
+            )
+            complex_output = await complex_llm_node(complex_input)
+            print(""Complex Test Output:"", complex_output)
+
+            # Test with base URL set
+            os.environ[""OPENAI_BASE_URL""] = ""https://api.openai.com/v1/""
+            simple_output_with_base = await simple_llm_node(simple_input)
+            print(""Simple Test Output (with base URL):"", simple_output_with_base)
+        finally:
+            # Restore original env var state
+            if original_base_url is not None:
+                os.environ[""OPENAI_BASE_URL""] = original_base_url
+            elif ""OPENAI_BASE_URL"" in os.environ:
+                del os.environ[""OPENAI_BASE_URL""]
 
     asyncio.run(test_llm_nodes())