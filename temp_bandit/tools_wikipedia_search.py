@@ -22,7 +22,7 @@
 # ### Agent Configuration
 #
 # Configure an assistant agent and user proxy to be used for LLM recommendation and execution respectively.
-agentops.init(auto_start_session=False)
+agentops.init(auto_start_session=False, trace_name=""AG2 Wikipedia Search Tools"")
 tracer = agentops.start_trace(
     trace_name=""AG2 Wikipedia Search Tools"", tags=[""ag2-wikipedia-search-tools"", ""agentops-example""]
 )
@@ -70,3 +70,13 @@
 )
 
 agentops.end_trace(tracer, end_state=""Success"")
+
+# Let's check programmatically that spans were recorded in AgentOps
+print(""
"" + ""="" * 50)
+print(""Now let's verify that our LLM calls were tracked properly..."")
+try:
+    agentops.validate_trace_spans(trace_context=tracer)
+    print(""
✅ Success! All LLM spans were properly recorded in AgentOps."")
+except agentops.ValidationError as e:
+    print(f""
❌ Error validating spans: {e}"")
+    raise