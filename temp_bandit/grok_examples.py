@@ -17,8 +17,8 @@
 os.environ[""AGENTOPS_API_KEY""] = os.getenv(""AGENTOPS_API_KEY"", ""your_api_key_here"")
 
 # Next we initialize the AgentOps client.
-agentops.init(auto_start_session=False)
-tracer = agentops.start_trace(trace_name=""XAI Example"", tags=[""xai-example"", ""grok"", ""agentops-example""])
+agentops.init(auto_start_session=False, trace_name=""XAI Grok Example"", tags=[""xai"", ""grok"", ""agentops-example""])
+tracer = agentops.start_trace(trace_name=""XAI Grok Example"", tags=[""xai-example"", ""grok"", ""agentops-example""])
 
 # And we are all set! Note the seesion url above. We will use it to track the chatbot.
 #
@@ -77,4 +77,15 @@
 # Awesome! We can now transliterate from English to any language! And all of this can be tracked with AgentOps by going to the session url above.
 agentops.end_trace(tracer, end_state=""Success"")
 
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
+
+
 # We end the session with a success state and a success reason. This is useful if you want to track the success or failure of the chatbot. In that case you can set the end state to failure and provide a reason. By default the session will have an indeterminate end state.