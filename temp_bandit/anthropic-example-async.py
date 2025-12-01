@@ -22,7 +22,7 @@
 #
 # Now let's set the client as Anthropic and open an agentops trace!
 client = Anthropic()
-agentops.init(tags=[""anthropic-async"", ""agentops-example""])
+agentops.init(trace_name=""Anthropic Async Example"", tags=[""anthropic-async"", ""agentops-example""])
 # Now we create three personality presets;
 #
 # Legion is a relentless and heavy-hitting Titan that embodies brute strength and defensive firepower, Northstar is a precise and agile sniper that excels in long-range combat and flight, while Ronin is a swift and aggressive melee specialist who thrives on close-quarters hit-and-run tactics.
@@ -108,3 +108,14 @@ async def main():
 # Run the main function
 asyncio.run(main())
 # We can observe the trace in the AgentOps dashboard by going to the trace URL provided above.
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