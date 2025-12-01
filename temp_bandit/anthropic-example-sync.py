@@ -21,7 +21,7 @@
 os.environ[""ANTHROPIC_API_KEY""] = os.getenv(""ANTHROPIC_API_KEY"", ""your_anthropic_api_key_here"")
 # Now let's set the client as Anthropic and an AgentOps session!
 client = Anthropic()
-agentops.init(auto_start_session=False)
+agentops.init(auto_start_session=False, trace_name=""Anthropic Sync Example"")
 tracer = agentops.start_trace(trace_name=""Anthropic Sync Example"", tags=[""anthropic-example"", ""agentops-example""])
 # Remember that story we made earlier? As of writing, claude-3-5-sonnet-20240620 (the version we will be using) has a 150k word, 680k character length. We also get an 8192 context length. This is great because we can actually set an example for the script!
 #
@@ -110,3 +110,13 @@
 #
 # Now we will end the session with a success message. We can also end the session with a failure or intdeterminate status. By default, the session will be marked as indeterminate.
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