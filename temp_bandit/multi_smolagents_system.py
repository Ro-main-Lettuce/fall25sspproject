@@ -47,9 +47,10 @@
 os.environ[""AGENTOPS_API_KEY""] = os.getenv(""AGENTOPS_API_KEY"", ""your_api_key_here"")
 os.environ[""OPENAI_API_KEY""] = os.getenv(""OPENAI_API_KEY"", ""your_openai_api_key_here"")
 
-agentops.init(auto_start_session=False)
+agentops.init(auto_start_session=False, trace_name=""Smolagents Multi-Agent System"")
 tracer = agentops.start_trace(
-    trace_name=""Orchestrate a Multi-Agent System"", tags=[""smolagents"", ""example"", ""multi-agent"", ""agentops-example""]
+    trace_name=""Smolagents Multi-Agent System Orchestration"",
+    tags=[""smolagents"", ""example"", ""multi-agent"", ""agentops-example""],
 )
 model = LiteLLMModel(""openai/gpt-4o-mini"")
 # ## Create a Web Search Tool
@@ -82,7 +83,7 @@ def visit_webpage(url: str) -> str:
 
     except RequestException as e:
         return f""Error fetching the webpage: {str(e)}""
-    except Exception as e:
+    except agentops.ValidationError as e:
         return f""An unexpected error occurred: {str(e)}""
 
 
@@ -95,6 +96,8 @@ def visit_webpage(url: str) -> str:
 web_agent = ToolCallingAgent(
     tools=[DuckDuckGoSearchTool(), visit_webpage],
     model=model,
+    name=""web_research"",
+    description=""Runs web searches for you. Give it your query as an argument. Please NOTE that the argument name is `task`."",
 )
 
 manager_agent = CodeAgent(
@@ -111,4 +114,15 @@ def visit_webpage(url: str) -> str:
 print(answer)
 # Awesome! We've successfully run a multi-agent system. Let's end the agentops session with a ""Success"" state. You can also end the session with a ""Failure"" or ""Indeterminate"" state, which is set as default.
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