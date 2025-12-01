@@ -112,8 +112,8 @@ def create_dread_assessment_prompt(threats):
 def get_dread_assessment(api_key, model_name, prompt):
     client = OpenAI(api_key=api_key)
 
-    # For reasoning models (o1, o3-mini), use a structured system prompt
-    if model_name in [""o1"", ""o3-mini""]:
+    # For reasoning models (o1, o3-mini, o3, o4-mini), use a structured system prompt
+    if model_name in [""o1"", ""o3-mini"", ""o3"", ""o4-mini""]:
         system_prompt = create_reasoning_system_prompt(
             task_description=""Perform a DREAD risk assessment for the identified security threats."",
             approach_description=""""""1. For each threat in the provided threat model:
@@ -189,30 +189,94 @@ def get_dread_assessment_azure(azure_api_endpoint, azure_api_key, azure_api_vers
 def get_dread_assessment_google(google_api_key, google_model, prompt):
     genai.configure(api_key=google_api_key)
     
-    model = genai.GenerativeModel(google_model)
+    # Check if we're using a model with thinking mode
+    is_thinking_mode = ""thinking"" in google_model.lower()
     
-    # Create the system message
-    system_message = ""You are a helpful assistant designed to output JSON. Only provide the DREAD risk assessment in JSON format with no additional text. Do not wrap the output in a code block.""
+    # If using thinking mode, use the actual model name without the ""thinking"" suffix
+    actual_model = google_model.replace(""-thinking"", """") if is_thinking_mode else google_model
     
-    # Start a chat session with the system message in the history
-    chat = model.start_chat(history=[
-        {""role"": ""user"", ""parts"": [system_message]},
-        {""role"": ""model"", ""parts"": [""Understood. I will provide DREAD risk assessments in JSON format only and will not wrap the output in a code block.""]}
-    ])
+    # Configure the generation based on whether thinking mode is enabled
+    generation_config = {
+        ""response_mime_type"": ""application/json""
+    }
     
-    # Send the actual prompt
-    response = chat.send_message(
-        prompt, 
-        safety_settings={
-            'DANGEROUS': 'block_only_high' # Set safety filter to allow generation of DREAD risk assessments
-        })
+    # Set up thinking configuration if using thinking mode
+    if is_thinking_mode:
+        thinking_config = {
+            ""enabled"": True,
+            ""budget_tokens"": 16000
+        }
+    else:
+        thinking_config = None
+        
+    model = genai.GenerativeModel(
+        actual_model,
+        generation_config=genai.types.GenerationConfig(**generation_config),
+        safety_settings={""DANGEROUS"":""block_only_high""}
+    )
     
     try:
-        # Access the JSON content from the response
-        dread_assessment = json.loads(response.text)
-        return dread_assessment
-    except json.JSONDecodeError:
-        return {}
+        # Create the system message
+        system_message = ""You are a helpful assistant designed to output JSON. Only provide the DREAD risk assessment in JSON format with no additional text. Do not wrap the output in a code block.""
+        
+        # Start a chat session with the system message in the history
+        chat = model.start_chat(history=[
+            {""role"": ""user"", ""parts"": [system_message]},
+            {""role"": ""model"", ""parts"": [""Understood. I will provide DREAD risk assessments in JSON format only and will not wrap the output in a code block.""]}
+        ])
+        
+        # Send the actual prompt with thinking configuration if enabled
+        response = chat.send_message(
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
+            # Access the JSON content from the response
+            dread_assessment = json.loads(response.text)
+            return dread_assessment
+        except json.JSONDecodeError:
+            # Create a fallback response
+            fallback_assessment = {
+                ""Risk Assessment"": [
+                    {
+                        ""Threat Type"": ""Error"",
+                        ""Scenario"": ""Failed to parse Google response"",
+                        ""Damage Potential"": 0,
+                        ""Reproducibility"": 0,
+                        ""Exploitability"": 0,
+                        ""Affected Users"": 0,
+                        ""Discoverability"": 0
+                    }
+                ]
+            }
+            return fallback_assessment
+            
+    except Exception as e:
+        error_message = str(e)
+        st.error(f""Error with Google AI API: {error_message}"")
+        
+        # Create a fallback response for API errors
+        fallback_assessment = {
+            ""Risk Assessment"": [
+                {
+                    ""Threat Type"": ""API Error"",
+                    ""Scenario"": f""Error calling Google AI API: {error_message}"",
+                    ""Damage Potential"": 0,
+                    ""Reproducibility"": 0,
+                    ""Exploitability"": 0,
+                    ""Affected Users"": 0,
+                    ""Discoverability"": 0
+                }
+            ]
+        }
+        return fallback_assessment
 
 # Function to get DREAD risk assessment from the Mistral model's response.
 def get_dread_assessment_mistral(mistral_api_key, mistral_model, prompt):
@@ -499,4 +563,4 @@ def get_dread_assessment_groq(groq_api_key, groq_model, prompt):
         with st.expander(""View model's reasoning process"", expanded=False):
             st.write(reasoning)
 
-    return dread_assessment
\ No newline at end of file
+    return dread_assessment