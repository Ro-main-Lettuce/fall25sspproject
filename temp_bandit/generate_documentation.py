@@ -22,6 +22,22 @@
 <script type=""module"" src=""/scripts/button_heartbeat_animation.js""></script>
 <script type=""module"" src=""/scripts/adjust_api_dynamically.js""></script>""""""
 
+# Title overrides to reflect correct names
+TITLE_OVERRIDES = {
+    ""ag2"": ""AG2"",
+    ""autogen"": ""AutoGen"",
+    ""crewai"": ""CrewAI"",
+    ""google_adk"": ""Google ADK"",
+    ""google_genai"": ""Google GenAI"",
+    ""langchain"": ""LangChain"",
+    ""litellm"": ""LiteLLM"",
+    ""llamaindex"": ""LlamaIndex"",
+    ""openai"": ""OpenAI"",
+    ""openai_agents"": ""OpenAI Agents"",
+    ""watsonx"": ""WatsonX"",
+    ""xai"": ""xAI"",
+}
+
 
 def convert_notebook_to_markdown(notebook_path):
     """"""Convert Jupyter notebook to markdown using jupyter nbconvert.""""""
@@ -104,7 +120,14 @@ def generate_mdx_content(notebook_path, processed_content, frontmatter=None):
     if not frontmatter:
         # Generate new frontmatter
         folder_name = Path(notebook_path).parent.name
-        title = f""{folder_name.replace('_', ' ').title()} Example""
+
+        # Check for title override, otherwise use default title case conversion
+        if folder_name in TITLE_OVERRIDES:
+            base_title = TITLE_OVERRIDES[folder_name]
+        else:
+            base_title = folder_name.replace(""_"", "" "").title()
+
+        title = f""{base_title}""
 
         # Extract description from first heading or use default
         description = f""{title} example using AgentOps""