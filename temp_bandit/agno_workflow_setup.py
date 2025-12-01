@@ -16,7 +16,6 @@
 """"""
 
 from agno.agent import Agent, RunResponse
-import asyncio
 import agentops
 from dotenv import load_dotenv
 from agno.workflow import Workflow
@@ -27,7 +26,7 @@
 
 
 load_dotenv()
-agentops.init(auto_start_session=False, tags=[""agno-example"", ""workflow-setup""])
+agentops.init(auto_start_session=False, trace_name=""Agno Workflow Setup"", tags=[""agno-example"", ""workflow-setup""])
 
 
 class CacheWorkflow(Workflow):
@@ -113,5 +112,15 @@ def demonstrate_workflows():
     except Exception:
         agentops.end_trace(tracer, end_state=""Error"")
 
+    # Let's check programmatically that spans were recorded in AgentOps
+    print(""
"" + ""="" * 50)
+    print(""Now let's verify that our LLM calls were tracked properly..."")
+    try:
+        agentops.validate_trace_spans(trace_context=tracer)
+        print(""
✅ Success! All LLM spans were properly recorded in AgentOps."")
+    except agentops.ValidationError as e:
+        print(f""
❌ Error validating spans: {e}"")
+        raise
+
 
-asyncio.run(demonstrate_workflows())
+demonstrate_workflows()