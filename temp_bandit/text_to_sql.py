@@ -98,9 +98,9 @@ def sql_engine(query: str) -> str:
 os.environ[""AGENTOPS_API_KEY""] = os.getenv(""AGENTOPS_API_KEY"", ""your_api_key_here"")
 os.environ[""OPENAI_API_KEY""] = os.getenv(""OPENAI_API_KEY"", ""your_openai_api_key_here"")
 
-agentops.init(auto_start_session=False)
+agentops.init(auto_start_session=False, trace_name=""Smolagents Text-to-SQL"")
 tracer = agentops.start_trace(
-    trace_name=""Text-to-SQL"", tags=[""smolagents"", ""example"", ""text-to-sql"", ""agentops-example""]
+    trace_name=""Smolagents Text-to-SQL"", tags=[""smolagents"", ""example"", ""text-to-sql"", ""agentops-example""]
 )
 model = LiteLLMModel(""openai/gpt-4o-mini"")
 agent = CodeAgent(
@@ -156,4 +156,15 @@ def sql_engine(query: str) -> str:
 agent.run(""Which waiter got more total money from tips?"")
 # All done! Now we can end the agentops session with a ""Success"" state. You can also end the session with a ""Failure"" or ""Indeterminate"" state, where the ""Indeterminate"" state is used by default.
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
+
 # You can view the session in the [AgentOps dashboard](https://app.agentops.ai/sessions) by clicking the link provided after ending the session.