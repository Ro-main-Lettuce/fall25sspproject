@@ -77,3 +77,17 @@ def find_movie(genre: str) -> str:
 
 # ## Check your session
 # Finally, check your run on [AgentOps](https://app.agentops.ai). You will see a session recorded with the LLM calls and tool usage.
+
+# Let's check programmatically that spans were recorded in AgentOps
+print(""
"" + ""="" * 50)
+print(""Now let's verify that our LLM calls were tracked properly..."")
+try:
+    import agentops
+
+    agentops.validate_trace_spans(trace_context=None)
+    print(""
✅ Success! All LLM spans were properly recorded in AgentOps."")
+except ImportError:
+    print(""
❌ Error: agentops library not installed. Please install it to validate spans."")
+except agentops.ValidationError as e:
+    print(f""
❌ Error validating spans: {e}"")
+    raise