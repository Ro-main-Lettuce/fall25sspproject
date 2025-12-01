@@ -26,7 +26,9 @@
 os.environ[""OPENAI_API_KEY""] = os.getenv(""OPENAI_API_KEY"", ""your_openai_api_key_here"")
 os.environ[""AGENTOPS_API_KEY""] = os.getenv(""AGENTOPS_API_KEY"", ""your_api_key_here"")
 
-agentops.init(auto_start_session=True)
+agentops.init(
+    auto_start_session=False, trace_name=""OpenAI Web Search Example"", tags=[""openai"", ""web-search"", ""agentops-example""]
+)
 tracer = agentops.start_trace(
     trace_name=""OpenAI Responses Example"", tags=[""openai-responses-example"", ""openai"", ""agentops-example""]
 )
@@ -101,6 +103,17 @@
 print(json.dumps(response_multimodal.__dict__, default=lambda o: o.__dict__, indent=4))
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
 # In the above example, we were able to use the `web_search` tool to search the web for news related to the image in one API call instead of multiple round trips that would be required if we were using the Chat Completions API.
 # With the responses API
 # 🔥 a single API call can handle: