@@ -28,6 +28,7 @@
 from dotenv import load_dotenv
 import random
 import uuid
+import asyncio
 
 from pydantic import BaseModel
 import agentops
@@ -53,8 +54,12 @@
 os.environ[""AGENTOPS_API_KEY""] = os.getenv(""AGENTOPS_API_KEY"", ""your_api_key_here"")
 os.environ[""OPENAI_API_KEY""] = os.getenv(""OPENAI_API_KEY"", ""your_openai_api_key_here"")
 
-agentops.init(tags=[""customer-service-agent"", ""openai-agents"", ""agentops-example""], auto_start_session=False)
-tracer = agentops.start_trace(trace_name=""Customer Service Agent"")
+agentops.init(
+    trace_name=""OpenAI Agents Customer Service"",
+    tags=[""customer-service-agent"", ""openai-agents"", ""agentops-example""],
+    auto_start_session=False,
+)
+tracer = agentops.start_trace(trace_name=""OpenAI Agents Customer Service Agent"")
 
 
 # Context model for the airline agent
@@ -102,13 +107,13 @@ async def update_seat(context: RunContextWrapper[AirlineAgentContext], confirmat
     return f""Updated seat to {new_seat} for confirmation number {confirmation_number}""
 
 
-### HOOKS
+# HOOKS
 async def on_seat_booking_handoff(context: RunContextWrapper[AirlineAgentContext]) -> None:
     flight_number = f""FLT-{random.randint(100, 999)}""
     context.context.flight_number = flight_number
 
 
-### AGENTS
+# AGENTS
 faq_agent = Agent[AirlineAgentContext](
     name=""FAQ Agent"",
     handoff_description=""A helpful agent that can answer questions about the airline."",
@@ -162,30 +167,60 @@ async def main():
     # Here, we'll just use a random UUID for the conversation ID
     conversation_id = uuid.uuid4().hex[:16]
 
-    while True:
-        user_input = input(""Enter your message: "")
+    # Predefined test messages to demonstrate the customer service agent
+    test_messages = [
+        ""Hello, I need help with my flight"",
+        ""I want to change my seat"",
+        ""My confirmation number is ABC123"",
+        ""I'd like seat 12A please"",
+        ""What's the baggage policy?"",
+        ""How many seats are on the plane?"",
+        ""Is there wifi on the flight?"",
+        ""Thank you for your help"",
+    ]
+
+    print(""🤖 Starting Customer Service Agent Demo"")
+    print(""="" * 50)
+
+    for user_input in test_messages:
+        print(f""
👤 User: {user_input}"")
+
         with trace(""Customer service"", group_id=conversation_id):
             input_items.append({""content"": user_input, ""role"": ""user""})
             result = await Runner.run(current_agent, input_items, context=context)
 
             for new_item in result.new_items:
                 agent_name = new_item.agent.name
                 if isinstance(new_item, MessageOutputItem):
-                    print(f""{agent_name}: {ItemHelpers.text_message_output(new_item)}"")
+                    print(f""🤖 {agent_name}: {ItemHelpers.text_message_output(new_item)}"")
                 elif isinstance(new_item, HandoffOutputItem):
-                    print(f""Handed off from {new_item.source_agent.name} to {new_item.target_agent.name}"")
+                    print(f""🔄 Handed off from {new_item.source_agent.name} to {new_item.target_agent.name}"")
                 elif isinstance(new_item, ToolCallItem):
-                    print(f""{agent_name}: Calling a tool"")
+                    print(f""🔧 {agent_name}: Calling a tool"")
                 elif isinstance(new_item, ToolCallOutputItem):
-                    print(f""{agent_name}: Tool call output: {new_item.output}"")
+                    print(f""🔧 {agent_name}: Tool call output: {new_item.output}"")
                 else:
-                    print(f""{agent_name}: Skipping item: {new_item.__class__.__name__}"")
+                    print(f""ℹ️  {agent_name}: Skipping item: {new_item.__class__.__name__}"")
             input_items = result.to_input_list()
             current_agent = result.last_agent
 
+    print(""
"" + ""="" * 50)
+    print(""🎉 Customer Service Agent Demo Complete!"")
+
+
+if __name__ == ""__main__"":
+    asyncio.run(main())
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
 
-# await main()
-agentops.end_trace(tracer, status=""Success"")
 
 # ## Conclusion
 #