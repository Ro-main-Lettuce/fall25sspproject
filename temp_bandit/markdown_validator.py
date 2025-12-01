@@ -24,7 +24,7 @@
 os.environ[""OPENAI_API_KEY""] = os.getenv(""OPENAI_API_KEY"", ""your_openai_api_key_here"")
 
 # The first step in any AgentOps integration is to call `agentops.init()`
-agentops.init(tags=[""markdown_validator"", ""agentops-example""])
+agentops.init(trace_name=""CrewAI Markdown Validator"", tags=[""markdown_validator"", ""agentops-example""])
 
 
 # Lets start by creating our markdown validator tool
@@ -104,3 +104,14 @@ def markdown_validation_tool(file_path: str) -> str:
 
 # Now lets run our task!
 syntax_review_task.execute_sync()
+
+
+# Let's check programmatically that spans were recorded in AgentOps
+print(""
"" + ""="" * 50)
+print(""Now let's verify that our LLM calls were tracked properly..."")
+try:
+    agentops.validate_trace_spans(trace_context=None)
+    print(""
✅ Success! All LLM spans were properly recorded in AgentOps."")
+except agentops.ValidationError as e:
+    print(f""
❌ Error validating spans: {e}"")
+    raise