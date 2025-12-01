@@ -17,7 +17,7 @@
 os.environ[""ANTHROPIC_API_KEY""] = os.getenv(""ANTHROPIC_API_KEY"", ""your_anthropic_api_key_here"")
 #
 # Now let's set the client as Anthropic and make an AgentOps trace
-agentops.init(tags=[""anthropic-example-tool-tutorials"", ""agentops-example""])
+agentops.init(trace_name=""Anthropic Understanding Tools"", tags=[""anthropic-example-tool-tutorials"", ""agentops-example""])
 client = Anthropic()
 # Now to create a simple dummy tool! We are going to make a tool that will tell us about the demon infestation levels for 3 areas. From there, we will have VEGA, our AI determine the best place for the Doom Slayer to attack.
 locations = [
@@ -371,3 +371,14 @@ def inventoryscan():
 
 message = response.content[0].text
 print(message)
+
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