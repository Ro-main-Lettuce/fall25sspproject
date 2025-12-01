@@ -20,7 +20,9 @@
 os.environ[""SERPER_API_KEY""] = os.getenv(""SERPER_API_KEY"", ""your_serper_api_key_here"")
 
 # Initialize AgentOps client
-agentops.init(auto_start_session=False)
+agentops.init(
+    auto_start_session=False, trace_name=""CrewAI Job Posting"", tags=[""crewai"", ""job-posting"", ""agentops-example""]
+)
 
 web_search_tool = WebsiteSearchTool()
 serper_dev_tool = SerperDevTool()
@@ -133,10 +135,10 @@ def industry_analysis_task(self, agent, company_domain, company_description):
 tracer = agentops.start_trace(trace_name=""CrewAI Job Posting"", tags=[""crew-job-posting-example"", ""agentops-example""])
 tasks = Tasks()
 agents = Agents()
-company_description = input(""What is the company description?
"")
-company_domain = input(""What is the company domain?
"")
-hiring_needs = input(""What are the hiring needs?
"")
-specific_benefits = input(""What are specific_benefits you offer?
"")
+company_description = ""We are a software company that builds AI-powered tools for businesses.""
+company_domain = ""https://www.agentops.ai""
+hiring_needs = ""We are looking for a software engineer with 3 years of experience in Python and Django.""
+specific_benefits = ""We offer a competitive salary, health insurance, and a 401k plan.""
 
 # Create Agents
 researcher_agent = agents.research_agent()
@@ -172,3 +174,13 @@ def industry_analysis_task(self, agent, company_domain, company_description):
 print(result)
 
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