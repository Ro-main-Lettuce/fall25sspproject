@@ -30,8 +30,8 @@ def create_mitigations_prompt(threats):
 def get_mitigations(api_key, model_name, prompt):
     client = OpenAI(api_key=api_key)
 
-    # For reasoning models (o1, o3-mini), use a structured system prompt
-    if model_name in [""o1"", ""o3-mini""]:
+    # For reasoning models (o1, o3-mini, o3, o4-mini), use a structured system prompt
+    if model_name in [""o1"", ""o3-mini"", ""o3"", ""o4-mini""]:
         system_prompt = create_reasoning_system_prompt(
             task_description=""Generate effective security mitigations for the identified threats using the STRIDE methodology."",
             approach_description=""""""1. Analyze each threat in the provided threat model
@@ -87,21 +87,76 @@ def get_mitigations_azure(azure_api_endpoint, azure_api_key, azure_api_version,
 # Function to get mitigations from the Google model's response.
 def get_mitigations_google(google_api_key, google_model, prompt):
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
         system_instruction=""You are a helpful assistant that provides threat mitigation strategies in Markdown format."",
+        safety_settings={""DANGEROUS"":""block_only_high""}
     )
-    response = model.generate_content(prompt)
+    
     try:
-        # Extract the text content from the 'candidates' attribute
-        mitigations = response.candidates[0].content.parts[0].text
-        # Replace '
' with actual newline characters
-        mitigations = mitigations.replace('\
', '
')
-    except (IndexError, AttributeError) as e:
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
+        try:
+            # Extract the text content from the 'candidates' attribute
+            mitigations = response.candidates[0].content.parts[0].text
+            # Replace '
' with actual newline characters
+            mitigations = mitigations.replace('\
', '
')
+            return mitigations
+        except (IndexError, AttributeError) as e:
+            # Create a fallback response for parsing errors
+            fallback_mitigations = """"""
+## Error Generating Mitigations
 
-        return None
+**Error:** Failed to parse Google response
 
-    return mitigations
+### Suggestions:
+- Try again with a different model
+- Simplify the input or break it into smaller components
+- Check if the model is available and properly configured
+""""""
+            return fallback_mitigations
+            
+    except Exception as e:
+        error_message = str(e)
+        st.error(f""Error with Google AI API: {error_message}"")
+        
+        # Create a fallback response for API errors
+        fallback_mitigations = f""""""
+## Error Generating Mitigations
+
+**API Error:** {error_message}
+
+### Suggestions:
+- For complex applications, try simplifying the input or breaking it into smaller components
+- If you're using extended thinking mode and encountering timeouts, try the standard model instead
+- Consider reducing the complexity of the application description
+""""""
+        return fallback_mitigations
 
 # Function to get mitigations from the Mistral model's response.
 def get_mitigations_mistral(mistral_api_key, mistral_model, prompt):
@@ -289,4 +344,4 @@ def get_mitigations_groq(groq_api_key, groq_model, prompt):
         with st.expander(""View model's reasoning process"", expanded=False):
             st.write(reasoning)
 
-    return mitigations
\ No newline at end of file
+    return mitigations