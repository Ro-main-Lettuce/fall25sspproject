@@ -151,8 +151,8 @@ def get_image_analysis(api_key, model_name, prompt, base64_image):
 def get_threat_model(api_key, model_name, prompt):
     client = OpenAI(api_key=api_key)
 
-    # For reasoning models (o1, o3-mini), use a structured system prompt
-    if model_name in [""o1"", ""o3-mini""]:
+    # For reasoning models (o1, o3-mini, o3, o4-mini), use a structured system prompt
+    if model_name in [""o1"", ""o3-mini"", ""o3"", ""o4-mini""]:
         system_prompt = create_reasoning_system_prompt(
             task_description=""Analyze the provided application description and generate a comprehensive threat model using the STRIDE methodology."",
             approach_description=""""""1. Carefully read and understand the application description
@@ -224,22 +224,77 @@ def get_threat_model_azure(azure_api_endpoint, azure_api_key, azure_api_version,
 # Function to get threat model from the Google response.
 def get_threat_model_google(google_api_key, google_model, prompt):
     genai.configure(api_key=google_api_key)
+    
+    # Check if we're using a model with thinking mode
+    is_thinking_mode = ""thinking"" in google_model.lower()
+    
+    # If using thinking mode, use the actual model name without the ""thinking"" suffix
+    actual_model = google_model.replace(""-thinking"", """") if is_thinking_mode else google_model
+    
+    # Configure the generation based on whether thinking mode is enabled
+    generation_config = {
+        ""response_mime_type"": ""application/json""
+    }
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
-        generation_config={""response_mime_type"": ""application/json""})
-    response = model.generate_content(
-        prompt,
-        safety_settings={
-            'DANGEROUS': 'block_only_high' # Set safety filter to allow generation of threat models
-        })
+        actual_model,
+        generation_config=genai.types.GenerationConfig(**generation_config),
+        safety_settings={""DANGEROUS"":""block_only_high""}
+    )
+    
     try:
-        # Access the JSON content from the 'parts' attribute of the 'content' object
-        response_content = json.loads(response.candidates[0].content.parts[0].text)
-    except json.JSONDecodeError:
-
-        return None
-
-    return response_content
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
+            # Access the JSON content from the 'parts' attribute of the 'content' object
+            response_content = json.loads(response.candidates[0].content.parts[0].text)
+            return response_content
+        except json.JSONDecodeError:
+            # Create a fallback response for JSON parsing errors
+            fallback_response = {
+                ""Threat Model"": [
+                    {
+                        ""Threat Type"": ""Error"",
+                        ""Scenario"": ""Failed to parse Google response"",
+                        ""Description"": ""The model response could not be parsed as valid JSON.""
+                    }
+                ]
+            }
+            return fallback_response
+            
+    except Exception as e:
+        error_message = str(e)
+        st.error(f""Error with Google AI API: {error_message}"")
+        
+        # Create a fallback response for API errors
+        fallback_response = {
+            ""Threat Model"": [
+                {
+                    ""Threat Type"": ""API Error"",
+                    ""Scenario"": f""Error calling Google AI API: {error_message}"",
+                    ""Description"": ""An error occurred while communicating with the Google AI API.""
+                }
+            ]
+        }
+        return fallback_response
 
 # Function to get threat model from the Mistral response.
 def get_threat_model_mistral(mistral_api_key, mistral_model, prompt):
@@ -504,4 +559,4 @@ def get_threat_model_groq(groq_api_key, groq_model, prompt):
         with st.expander(""View model's reasoning process"", expanded=False):
             st.write(reasoning)
 
-    return response_content
\ No newline at end of file
+    return response_content