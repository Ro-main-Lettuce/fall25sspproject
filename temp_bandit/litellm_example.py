@@ -28,7 +28,7 @@
     ""OPENAI_API_KEY"", ""your_openai_api_key_here""
 )  # or the provider of your choosing
 
-agentops.init(auto_start_session=False)
+agentops.init(auto_start_session=False, trace_name=""LiteLLM Example"")
 tracer = agentops.start_trace(trace_name=""LiteLLM Example"", tags=[""litellm-example"", ""agentops-example""])
 
 # Note: AgentOps requires that you call LiteLLM completions differently than the LiteLLM's docs mention
@@ -46,7 +46,17 @@
 # litellm.completion()
 # ```
 messages = [{""role"": ""user"", ""content"": ""Write a 12 word poem about secret agents.""}]
-response = litellm.completion(model=""gpt-4"", messages=messages)  # or the model of your choosing
+response = litellm.completion(model=""gpt-4o-mini"", messages=messages)  # or the model of your choosing
 print(response.choices[0].message.content)
 
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