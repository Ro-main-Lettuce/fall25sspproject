@@ -11,9 +11,6 @@
 import asyncio
 import os
 from dotenv import load_dotenv
-from IPython.core.error import (
-    StdinNotImplementedError,
-)
 
 import agentops
 
@@ -32,7 +29,7 @@
 os.environ[""AGENTOPS_API_KEY""] = os.getenv(""AGENTOPS_API_KEY"", ""your_api_key_here"")
 os.environ[""OPENAI_API_KEY""] = os.getenv(""OPENAI_API_KEY"", ""your_openai_api_key_here"")
 
-agentops.init(auto_start_session=False)
+agentops.init(auto_start_session=False, trace_name=""Autogen Math Agent Example"")
 tracer = agentops.start_trace(
     trace_name=""Microsoft Autogen Tool Example"", tags=[""autogen-tool"", ""microsoft-autogen"", ""agentops-example""]
 )
@@ -97,15 +94,22 @@ async def main():
 
         agentops.end_trace(tracer, end_state=""Success"")
 
-    except StdinNotImplementedError:
-        print(""StdinNotImplementedError: This typically happens in non-interactive environments."")
-        agentops.end_trace(tracer, end_state=""Indeterminate"")
     except Exception as e:
         print(f""An error occurred: {e}"")
         agentops.end_trace(tracer, end_state=""Error"")
     finally:
         await model_client.close()
 
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
 
 if __name__ == ""__main__"":
     try: