@@ -15,7 +15,7 @@
 os.environ[""GEMINI_API_KEY""] = os.getenv(""GEMINI_API_KEY"", ""your_gemini_api_key_here"")
 
 # Initialize AgentOps and Gemini client
-agentops.init(tags=[""gemini-example"", ""agentops-example""])
+agentops.init(trace_name=""Google Gemini Example"", tags=[""gemini-example"", ""agentops-example""])
 client = genai.Client()
 
 # Test synchronous generation
@@ -46,3 +46,13 @@
     model=""gemini-1.5-flash"", contents=""This is a test sentence to count tokens.""
 )
 print(f""Token count: {token_response.total_tokens}"")
+
+# Let's check programmatically that spans were recorded in AgentOps
+print(""
"" + ""="" * 50)
+print(""Now let's verify that our LLM calls were tracked properly..."")
+try:
+    agentops.validate_trace_spans(trace_context=None)
+    print(""
✅ Success! All LLM spans were properly recorded in AgentOps."")
+except agentops.ValidationError as e:
+    print(f""
❌ Error validating spans: {e}"")
+    raise