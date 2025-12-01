@@ -21,7 +21,7 @@
 os.environ[""AGENTOPS_API_KEY""] = os.getenv(""AGENTOPS_API_KEY"", ""your_api_key_here"")
 
 # Next we initialize the AgentOps client.
-agentops.init(auto_start_session=True)
+agentops.init(auto_start_session=True, trace_name=""OpenAI Async Example"", tags=[""openai"", ""async"", ""agentops-example""])
 tracer = agentops.start_trace(
     trace_name=""OpenAI Async Example"", tags=[""openai-async-example"", ""openai"", ""agentops-example""]
 )
@@ -37,7 +37,10 @@
 """"""
 
 user_prompt = [
-    {""type"": ""text"", ""text"": ""Write a mystery thriller story based on your understanding of the provided image.""},
+    {
+        ""type"": ""text"",
+        ""text"": ""Write a very short mystery thriller story based on your understanding of the provided image."",
+    },
     {
         ""type"": ""image_url"",
         ""image_url"": {""url"": ""https://www.cosy.sbg.ac.at/~pmeerw/Watermarking/lena_color.gif""},
@@ -78,5 +81,16 @@ async def main_stream():
 asyncio.run(main_stream())
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
 # Note that the response is a generator that yields chunks of the story. We can track this with AgentOps by navigating to the trace url and viewing the run.
 # All done!