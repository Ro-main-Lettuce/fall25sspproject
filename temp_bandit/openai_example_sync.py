@@ -20,7 +20,7 @@
 os.environ[""AGENTOPS_API_KEY""] = os.getenv(""AGENTOPS_API_KEY"", ""your_api_key_here"")
 
 # Next we initialize the AgentOps client.
-agentops.init(auto_start_session=True)
+agentops.init(auto_start_session=True, trace_name=""OpenAI Sync Example"", tags=[""openai"", ""sync"", ""agentops-example""])
 tracer = agentops.start_trace(
     trace_name=""OpenAI Sync Example"", tags=[""openai-sync-example"", ""openai"", ""agentops-example""]
 )
@@ -35,7 +35,7 @@
 You are given a prompt and you need to generate a story based on the prompt.
 """"""
 
-user_prompt = ""Write a story about a cyber-warrior trapped in the imperial time period.""
+user_prompt = ""Write a very short story about a cyber-warrior trapped in the imperial time period.""
 
 messages = [
     {""role"": ""system"", ""content"": system_prompt},
@@ -64,5 +64,15 @@
 
 agentops.end_trace(tracer, end_state=""Success"")
 
+# Let's check programmatically that spans were recorded in AgentOps
+print(""
"" + ""="" * 50)
+print(""Now let's verify that our LLM calls were tracked properly..."")
+try:
+    result = agentops.validate_trace_spans(trace_context=tracer)
+    agentops.print_validation_summary(result)
+except agentops.ValidationError as e:
+    print(f""
❌ Error validating spans: {e}"")
+    raise
+
 # Note that the response is a generator that yields chunks of the story. We can track this with AgentOps by navigating to the trace url and viewing the run.
 # All done!