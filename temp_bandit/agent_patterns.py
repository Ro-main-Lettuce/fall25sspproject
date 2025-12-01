@@ -78,7 +78,15 @@
 os.environ[""OPENAI_API_KEY""] = os.getenv(""OPENAI_API_KEY"", ""your_openai_api_key_here"")
 
 # Initialize AgentOps
-agentops.init(auto_start_session=False)
+agentops.init(
+    auto_start_session=False,
+    trace_name=""OpenAI Agents Patterns"",
+    tags=[""openai-agents"", ""patterns"", ""agentops-example""],
+)
+tracer = agentops.start_trace(
+    trace_name=""OpenAI Agents Patterns"",
+    tags=[""openai-agents"", ""patterns"", ""agentops-example""],
+)
 # Note: tracer will be defined in each section's cell for clarity, using the specific tags for that pattern.
 # ## 1. Agents as Tools Pattern
 #
@@ -87,8 +95,7 @@
 # For example, you could model the translation task above as tool calls instead: rather than handing over to the language-specific agent, you could call the agent as a tool, and then use the result in the next step. This enables things like translating multiple languages at once.
 #
 # This pattern demonstrates using agents as callable tools within other agents. The orchestrator agent receives a user message and then picks which specialized agents to call as tools.
-# Start the AgentOps trace session
-tracer = agentops.start_trace(trace_name=""Agents as Tools Pattern"", tags=[""agentops-example"", ""openai-agents""])
+# Agents as Tools Pattern Example
 
 # Define specialized translation agents
 spanish_agent = Agent(
@@ -159,9 +166,6 @@ async def run_agents_as_tools_demo():
 
 # Run the demo
 # await run_agents_as_tools_demo()
-
-# End the AgentOps trace session
-agentops.end_trace(tracer, end_state=""Success"")
 # ## 2. Deterministic Flow Pattern
 #
 # A common tactic is to break down a task into a series of smaller steps. Each task can be performed by an agent, and the output of one agent is used as input to the next. For example, if your task was to generate a story, you could break it down into the following steps:
@@ -173,8 +177,7 @@ async def run_agents_as_tools_demo():
 # Each of these steps can be performed by an agent. The output of one agent is used as input to the next.
 #
 # This pattern demonstrates breaking down a complex task into a series of smaller, sequential steps. Each step is performed by an agent, and the output of one agent is used as input to the next.
-# Start the AgentOps trace session
-tracer = agentops.start_trace(trace_name=""Deterministic Flow Pattern"", tags=[""agentops-example"", ""openai-agents""])
+# Deterministic Flow Pattern Example
 
 # Define the story generation workflow
 story_outline_agent = Agent(
@@ -232,9 +235,6 @@ async def run_deterministic_flow_demo():
 
 # Run the demo
 # await run_deterministic_flow_demo()
-
-# End the AgentOps trace session
-agentops.end_trace(tracer, end_state=""Success"")
 # ## 3. Forcing Tool Use Pattern
 #
 # This pattern shows how to force an agent to use a tool using `ModelSettings(tool_choice=\""required\"")`. This is useful when you want to ensure the agent always uses a specific tool rather than generating a response directly.
@@ -245,8 +245,7 @@ async def run_deterministic_flow_demo():
 # 3. `custom`: A custom tool use behavior function is used. The custom function receives all the tool results, and chooses to use the first tool result to generate the final output.
 #
 # For this demo, we'll allow the user to choose which tool use behavior to test:
-# Start the AgentOps trace session
-tracer = agentops.start_trace(trace_name=""Forcing Tool Use Pattern"", tags=[""agentops-example"", ""openai-agents""])
+# Forcing Tool Use Pattern Example
 
 
 # Define the weather tool and agent
@@ -269,25 +268,6 @@ async def custom_tool_use_behavior(
     return ToolsToFinalOutputResult(is_final_output=True, final_output=f""{weather.city} is {weather.conditions}."")
 
 
-# User can choose which behavior to test
-print(""Choose tool use behavior:"")
-print(""1. default - Send tool output to LLM"")
-print(""2. first_tool - Use first tool result as final output"")
-print(""3. custom - Use custom tool behavior function"")
-
-choice = input(""Enter choice (1, 2, or 3): "").strip()
-
-if choice == ""1"":
-    tool_use_behavior = ""default""
-elif choice == ""2"":
-    tool_use_behavior = ""first_tool""
-elif choice == ""3"":
-    tool_use_behavior = ""custom""
-else:
-    tool_use_behavior = ""default""
-    print(""Invalid choice, using default"")
-
-
 async def run_forcing_tool_use_demo(tool_use_behavior: str):
     print(f""Testing {tool_use_behavior} behavior:"")
 
@@ -310,11 +290,22 @@ async def run_forcing_tool_use_demo(tool_use_behavior: str):
     print(f""Result: {result.final_output}"")
 
 
-# Run the demo
-# await run_forcing_tool_use_demo(tool_use_behavior)
+async def run_all_forcing_tool_use_demos():
+    """"""Run all three tool use behavior demos automatically""""""
+    print(""Running all tool use behavior demos:"")
+    print(""1. default - Send tool output to LLM"")
+    print(""2. first_tool - Use first tool result as final output"")
+    print(""3. custom - Use custom tool behavior function"")
+    print()
 
-# End the AgentOps trace session
-agentops.end_trace(tracer, end_state=""Success"")
+    # Test all three behaviors
+    for behavior in [""default"", ""first_tool"", ""custom""]:
+        await run_forcing_tool_use_demo(behavior)
+        print(""-"" * 50)
+
+
+# Run the demo
+# await run_all_forcing_tool_use_demos()
 # ## 4. Input Guardrails Pattern
 #
 # Related to parallelization, you often want to run input guardrails to make sure the inputs to your agents are valid. For example, if you have a customer support agent, you might want to make sure that the user isn't trying to ask for help with a math problem.
@@ -324,8 +315,7 @@ async def run_forcing_tool_use_demo(tool_use_behavior: str):
 # This is really useful for latency: for example, you might have a very fast model that runs the guardrail and a slow model that runs the actual agent. You wouldn't want to wait for the slow model to finish, so guardrails let you quickly reject invalid inputs.
 #
 # This pattern demonstrates how to use input guardrails to validate user inputs before they reach the main agent. Guardrails can prevent inappropriate or off-topic requests from being processed.
-# Start the AgentOps trace session
-tracer = agentops.start_trace(trace_name=""Input Guardrails Pattern"", tags=[""agentops-example"", ""openai-agents""])
+# Input Guardrails Pattern Example
 
 
 # Define the guardrail
@@ -377,18 +367,14 @@ async def run_input_guardrails_demo():
 
 # Run the demo
 # await run_input_guardrails_demo()
-
-# End the AgentOps trace session
-agentops.end_trace(tracer, end_state=""Success"")
 # ## 5. LLM as a Judge Pattern
 #
 # LLMs can often improve the quality of their output if given feedback. A common pattern is to generate a response using a model, and then use a second model to provide feedback. You can even use a small model for the initial generation and a larger model for the feedback, to optimize cost.
 #
 # For example, you could use an LLM to generate an outline for a story, and then use a second LLM to evaluate the outline and provide feedback. You can then use the feedback to improve the outline, and repeat until the LLM is satisfied with the outline.
 #
 # This pattern shows how to use one LLM to evaluate and improve the output of another. The first agent generates content, and the second agent judges the quality and provides feedback for improvement.
-# Start the AgentOps trace session
-tracer = agentops.start_trace(trace_name=""LLM as a Judge Pattern"", tags=[""agentops-example"", ""openai-agents""])
+# LLM as a Judge Pattern Example
 
 # Define the story generation and evaluation agents
 story_outline_generator = Agent(
@@ -457,18 +443,14 @@ async def run_llm_as_judge_demo():
 
 # Run the demo
 # await run_llm_as_judge_demo()
-
-# End the AgentOps trace session
-agentops.end_trace(tracer, end_state=""Success"")
 # ## 6. Output Guardrails Pattern
 #
 # Related to parallelization, you often want to run output guardrails to make sure the outputs from your agents are valid. Guardrails can have a \""tripwire\"" - if the tripwire is triggered, the agent execution will immediately stop and a `GuardrailTripwireTriggered` exception will be raised.
 #
 # This is really useful for latency: for example, you might have a very fast model that runs the guardrail and a slow model that runs the actual agent. You wouldn't want to wait for the slow model to finish, so guardrails let you quickly reject invalid outputs.
 #
 # This pattern demonstrates how to use output guardrails to validate agent outputs after they are generated. This can help prevent sensitive information from being shared or ensure outputs meet quality standards.
-# Start the AgentOps trace session
-tracer = agentops.start_trace(trace_name=""Output Guardrails Pattern"", tags=[""agentops-example"", ""openai-agents""])
+# Output Guardrails Pattern Example
 
 
 # The agent's output type
@@ -524,18 +506,14 @@ async def run_output_guardrails_demo():
 
 # Run the demo
 # await run_output_guardrails_demo()
-
-# End the AgentOps trace session
-agentops.end_trace(tracer, end_state=""Success"")
 # ## 7. Parallelization Pattern
 #
 # Running multiple agents in parallel is a common pattern. This can be useful for both latency (e.g. if you have multiple steps that don't depend on each other) and also for other reasons e.g. generating multiple responses and picking the best one.
 #
 # This example runs a translation agent multiple times in parallel, and then picks the best translation.
 #
 # This pattern shows how to run multiple agents in parallel to improve latency or generate multiple options to choose from. In this example, we run translation agents multiple times and pick the best result.
-# Start the AgentOps trace session
-tracer = agentops.start_trace(trace_name=""Output Guardrails Pattern"", tags=[""agentops-example"", ""openai-agents""])
+# Parallelization Pattern Example
 
 # Define agents for parallelization
 spanish_translation_agent = Agent(
@@ -581,18 +559,14 @@ async def run_parallelization_demo():
 
 # Run the demo
 # await run_parallelization_demo()
-
-# End the AgentOps trace session
-agentops.end_trace(tracer, end_state=""Success"")
 # ## 8. Routing Pattern
 #
 # In many situations, you have specialized sub-agents that handle specific tasks. You can use handoffs to route the task to the right agent.
 #
 # For example, you might have a frontline agent that receives a request, and then hands off to a specialized agent based on the language of the request.
 #
 # This pattern demonstrates handoffs and routing between specialized agents. The triage agent receives the first message and hands off to the appropriate agent based on the language of the request.
-# Start the AgentOps trace session
-tracer = agentops.start_trace(trace_name=""Routing Pattern"", tags=[""agentops-example"", ""openai-agents""])
+# Routing Pattern Example
 
 # Define language-specific agents
 french_routing_agent = Agent(
@@ -634,18 +608,14 @@ async def run_routing_demo():
 
 # Run the demo
 # await run_routing_demo()
-
-# End the AgentOps trace session
-agentops.end_trace(tracer, end_state=""Success"")
 # ## 9. Streaming Guardrails Pattern
 #
 # This example shows how to use guardrails as the model is streaming. Output guardrails run after the final output has been generated; this example runs guardrails every N tokens, allowing for early termination if bad output is detected.
 #
 # The expected output is that you'll see a bunch of tokens stream in, then the guardrail will trigger and stop the streaming.
 #
 # This pattern shows how to use guardrails during streaming to provide real-time validation. Unlike output guardrails that run after completion, streaming guardrails can interrupt the generation process early.
-# Start the AgentOps trace session
-tracer = agentops.start_trace(trace_name=""Streaming Guardrails Pattern"", tags=[""agentops-example"", ""openai-agents""])
+# Streaming Guardrails Pattern Example
 
 # Define streaming guardrail agent
 streaming_agent = Agent(
@@ -720,9 +690,20 @@ async def run_streaming_guardrails_demo():
 if __name__ == ""__main__"":
     # Run the streaming guardrails demo
     asyncio.run(run_streaming_guardrails_demo())
+    agentops.end_trace(tracer, end_state=""Success"")
+
+# Streaming Guardrails Pattern Example Complete
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
 
-# End the AgentOps trace session
-agentops.end_trace(tracer, end_state=""Success"")
 # ## Conclusion
 #
 # This notebook has demonstrated 9 key agent patterns that are commonly used in production AI applications. Each pattern showcases how agents can be orchestrated to perform complex tasks, validate inputs and outputs, and improve overall application performance.