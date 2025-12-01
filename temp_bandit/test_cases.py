@@ -37,8 +37,8 @@ def create_test_cases_prompt(threats):
 def get_test_cases(api_key, model_name, prompt):
     client = OpenAI(api_key=api_key)
 
-    # For reasoning models (o1, o3-mini), use a structured system prompt
-    if model_name in [""o1"", ""o3-mini""]:
+    # For reasoning models (o1, o3-mini, o3, o4-mini), use a structured system prompt
+    if model_name in [""o1"", ""o3-mini"", ""o3"", ""o4-mini""]:
         system_prompt = create_reasoning_system_prompt(
             task_description=""Generate comprehensive security test cases in Gherkin format for the identified threats."",
             approach_description=""""""1. Analyze each threat in the provided threat model:
@@ -110,16 +110,60 @@ def get_test_cases_azure(azure_api_endpoint, azure_api_key, azure_api_version, a
 # Function to get test cases from the Google model's response.
 def get_test_cases_google(google_api_key, google_model, prompt):
     genai.configure(api_key=google_api_key)
+    
+    # Check if we're using a model with thinking mode
+    is_thinking_mode = ""thinking"" in google_model.lower()
+    
+    # If using thinking mode, use the actual model name without the ""thinking"" suffix
+    actual_model = google_model.replace(""-thinking"", """") if is_thinking_mode else google_model
+    
+    # Set up thinking configuration if using thinking mode
+    if is_thinking_mode:
+        thinking_config = {
+            ""enabled"": True,
+            ""budget_tokens"": 16000
+        }
+    else:
+        thinking_config = None
+    
     model = genai.GenerativeModel(
-        google_model,
+        actual_model,
         system_instruction=""You are a helpful assistant that provides Gherkin test cases in Markdown format."",
+        safety_settings={""DANGEROUS"":""block_only_high""}
     )
-    response = model.generate_content(prompt)
     
-    # Access the content directly as the response will be in text format
-    test_cases = response.candidates[0].content.parts[0].text
+    try:
+        response = model.generate_content(
+            prompt,
+            thinking=thinking_config
+        )
+        
+        # Store thinking content in session state if available
+        if is_thinking_mode and hasattr(response, 'thinking'):
+            thinking_content = response.thinking
+            if thinking_content:
+                st.session_state['last_thinking_content'] = thinking_content
+        
+        # Access the content directly as the response will be in text format
+        test_cases = response.candidates[0].content.parts[0].text
+        return test_cases
+        
+    except Exception as e:
+        error_message = str(e)
+        st.error(f""Error with Google AI API: {error_message}"")
+        
+        # Create a fallback response for API errors
+        fallback_test_cases = f""""""
+## Error Generating Test Cases
 
-    return test_cases
+**API Error:** {error_message}
+
+### Suggestions:
+- For complex applications, try simplifying the input or breaking it into smaller components
+- If you're using extended thinking mode and encountering timeouts, try the standard model instead
+- Consider reducing the complexity of the application description
+""""""
+        return fallback_test_cases
 
 # Function to get test cases from the Mistral model's response.
 def get_test_cases_mistral(mistral_api_key, mistral_model, prompt):
@@ -312,4 +356,4 @@ def get_test_cases_groq(groq_api_key, groq_model, prompt):
         with st.expander(""View model's reasoning process"", expanded=False):
             st.write(reasoning)
 
-    return test_cases
\ No newline at end of file
+    return test_cases