@@ -126,7 +126,7 @@ def get_attack_tree(api_key, model_name, prompt):
     client = OpenAI(api_key=api_key)
 
     # For models that support JSON output format
-    if model_name in [""o1"", ""o3-mini""]:
+    if model_name in [""o1"", ""o3-mini"", ""o3"", ""o4-mini""]:
         system_prompt = create_reasoning_system_prompt(
             task_description=""Create a structured attack tree by analyzing potential attack paths."",
             approach_description=""""""Analyze the application and create an attack tree showing potential attack paths.
@@ -574,33 +574,81 @@ def create_attack_tree_schema_lm_studio():
 def get_attack_tree_google(google_api_key, google_model, prompt):
     genai.configure(api_key=google_api_key)
     
-    model = genai.GenerativeModel(google_model)
+    # Check if we're using a model with thinking mode
+    is_thinking_mode = ""thinking"" in google_model.lower()
     
-    # Create the system message
-    system_message = create_json_structure_prompt()
-    
-    # Start a chat session with the system message in the history
-    chat = model.start_chat(history=[
-        {""role"": ""user"", ""parts"": [system_message]},
-        {""role"": ""model"", ""parts"": [""Understood. I will provide attack tree data in JSON format only.""]}
-    ])
+    # If using thinking mode, use the actual model name without the ""thinking"" suffix
+    actual_model = google_model.replace(""-thinking"", """") if is_thinking_mode else google_model
     
-    # Configure safety settings to allow generation of attack trees
-    safety_settings = {
-        'HARASSMENT': 'BLOCK_NONE',
-        'HATE_SPEECH': 'BLOCK_NONE',
-        'SEXUALLY_EXPLICIT': 'BLOCK_NONE',
-        'DANGEROUS': 'BLOCK_NONE'
-    }
+    # Set up thinking configuration if using thinking mode
+    if is_thinking_mode:
+        thinking_config = {
+            ""enabled"": True,
+            ""budget_tokens"": 16000
+        }
+    else:
+        thinking_config = None
     
-    # Send the actual prompt with safety settings
-    response = chat.send_message(prompt, safety_settings=safety_settings)
+    # Create the model
+    model = genai.GenerativeModel(actual_model)
     
     try:
-        # Clean the response text and try to parse as JSON
-        cleaned_response = clean_json_response(response.text)
-        tree_data = json.loads(cleaned_response)
-        return convert_tree_to_mermaid(tree_data)
-    except (json.JSONDecodeError, AttributeError):
-        # Fallback: try to extract Mermaid code if JSON parsing fails
-        return extract_mermaid_code(response.text)
\ No newline at end of file
+        # Create the system message
+        system_message = create_json_structure_prompt()
+        
+        # Start a chat session with the system message in the history
+        chat = model.start_chat(history=[
+            {""role"": ""user"", ""parts"": [system_message]},
+            {""role"": ""model"", ""parts"": [""Understood. I will provide attack tree data in JSON format only.""]}
+        ])
+        
+        # Configure safety settings to allow generation of attack trees
+        safety_settings = {
+            'HARASSMENT': 'BLOCK_NONE',
+            'HATE_SPEECH': 'BLOCK_NONE',
+            'SEXUALLY_EXPLICIT': 'BLOCK_NONE',
+            'DANGEROUS': 'BLOCK_NONE'
+        }
+        
+        # Send the actual prompt with safety settings and thinking configuration
+        response = chat.send_message(
+            prompt, 
+            safety_settings=safety_settings,
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
+            # Clean the response text and try to parse as JSON
+            cleaned_response = clean_json_response(response.text)
+            tree_data = json.loads(cleaned_response)
+            return convert_tree_to_mermaid(tree_data)
+        except (json.JSONDecodeError, AttributeError):
+            # Fallback: try to extract Mermaid code if JSON parsing fails
+            try:
+                return extract_mermaid_code(response.text)
+            except:
+                # Create a fallback response if all parsing fails
+                fallback_mermaid = """"""
+graph TD
+    A[Error Parsing Response] --> B[API Response Could Not Be Processed]
+    B --> C[Try Again or Use Different Model]
+""""""
+                return fallback_mermaid
+                
+    except Exception as e:
+        error_message = str(e)
+        st.error(f""Error with Google AI API: {error_message}"")
+        
+        # Create a fallback response for API errors
+        fallback_mermaid = f""""""
+graph TD
+    A[API Error] --> B[{error_message}]
+    B --> C[Try Again or Use Different Model]
+""""""
+        return fallback_mermaid