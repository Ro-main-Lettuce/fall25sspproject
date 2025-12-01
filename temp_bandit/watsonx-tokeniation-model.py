@@ -15,7 +15,7 @@
 os.environ[""AGENTOPS_API_KEY""] = os.getenv(""AGENTOPS_API_KEY"", ""your_api_key_here"")
 
 # Initialize AgentOps
-agentops.init(tags=[""watsonx-tokenization"", ""agentops-example""])
+agentops.init(trace_name=""WatsonX Tokenization Model Example"", tags=[""watsonx-tokenization"", ""agentops-example""])
 # ## Initialize IBM Watsonx AI Credentials
 #
 # To use IBM Watsonx AI, you need to set up your credentials and project ID.
@@ -95,3 +95,13 @@
 # Close connections
 model.close_persistent_connection()
 llama_model.close_persistent_connection()
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