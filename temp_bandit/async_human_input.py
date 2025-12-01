@@ -1,8 +1,9 @@
-# Agent Chat with Async Human Inputs
+# Agent Chat with Async Operations
 #
-# We are going to create an agent that can chat with a human asynchronously. The agent will be able to respond to messages from the human and will also be able to send messages to the human.
+# We are going to create agents that can perform asynchronous operations and chat with each other.
+# This example demonstrates async capabilities without requiring human input.
 #
-# We are going to use AgentOps to monitor the agent's performance and observe its interactions with the human.
+# We are going to use AgentOps to monitor the agent's performance and observe their interactions.
 # # Install required dependencies
 # %pip install agentops
 # %pip install ag2
@@ -25,82 +26,124 @@
 os.environ[""AGENTOPS_API_KEY""] = os.getenv(""AGENTOPS_API_KEY"", ""your_api_key_here"")
 os.environ[""OPENAI_API_KEY""] = os.getenv(""OPENAI_API_KEY"", ""your_openai_api_key_here"")
 
-agentops.init(auto_start_session=False)
-tracer = agentops.start_trace(
-    trace_name=""AG2 Agent chat with Async Human Inputs"", tags=[""ag2-chat-async-human-inputs"", ""agentops-example""]
-)
+agentops.init(auto_start_session=False, trace_name=""AG2 Async Demo"")
+tracer = agentops.start_trace(trace_name=""AG2 Async Agent Demo"", tags=[""ag2-async-demo"", ""agentops-example""])
 
 
-# Define an asynchronous function that simulates some asynchronous task (e.g., I/O operation)
-async def my_asynchronous_function():
-    print(""Start asynchronous function"")
-    await asyncio.sleep(2)  # Simulate some asynchronous task (e.g., I/O operation)
-    print(""End asynchronous function"")
-    return ""input""
+# Define an asynchronous function that simulates async processing
+async def simulate_async_processing(task_name: str, delay: float = 1.0) -> str:
+    """"""
+    Simulate some asynchronous processing (e.g., API calls, file operations, etc.)
+    """"""
+    print(f""🔄 Starting async task: {task_name}"")
+    await asyncio.sleep(delay)  # Simulate async work
+    print(f""✅ Completed async task: {task_name}"")
+    return f""Processed: {task_name}""
 
 
-# Define a custom class `CustomisedUserProxyAgent` that extends `UserProxyAgent`
-class CustomisedUserProxyAgent(UserProxyAgent):
-    # Asynchronous function to get human input
+# Define a custom UserProxyAgent that simulates automated responses
+class AutomatedUserProxyAgent(UserProxyAgent):
+    def __init__(self, name: str, **kwargs):
+        super().__init__(name, **kwargs)
+        self.response_count = 0
+        self.predefined_responses = [
+            ""Yes, please generate interview questions for these topics."",
+            ""The questions look good. Can you make them more specific to senior-level positions?"",
+            ""Perfect! These questions are exactly what we need. Thank you!"",
+        ]
+
     async def a_get_human_input(self, prompt: str) -> str:
-        # Call the asynchronous function to get user input asynchronously
-        user_input = await my_asynchronous_function()
-        return user_input
+        # Simulate async processing before responding
+        await simulate_async_processing(f""Processing user input #{self.response_count + 1}"")
+
+        if self.response_count < len(self.predefined_responses):
+            response = self.predefined_responses[self.response_count]
+            self.response_count += 1
+            print(f""👤 User: {response}"")
+            return response
+        else:
+            print(""👤 User: TERMINATE"")
+            return ""TERMINATE""
 
-    # Asynchronous function to receive a message
     async def a_receive(
         self,
         message: Union[Dict, str],
         sender,
         request_reply: Optional[bool] = None,
         silent: Optional[bool] = False,
     ):
-        # Call the superclass method to handle message reception asynchronously
         await super().a_receive(message, sender, request_reply, silent)
 
 
-class CustomisedAssistantAgent(AssistantAgent):
-    # Asynchronous function to get human input
-    async def a_get_human_input(self, prompt: str) -> str:
-        # Call the asynchronous function to get user input asynchronously
-        user_input = await my_asynchronous_function()
-        return user_input
-
-    # Asynchronous function to receive a message
+class AsyncAssistantAgent(AssistantAgent):
     async def a_receive(
         self,
         message: Union[Dict, str],
         sender,
         request_reply: Optional[bool] = None,
         silent: Optional[bool] = False,
     ):
-        # Call the superclass method to handle message reception asynchronously
+        # Simulate async processing before responding
+        await simulate_async_processing(""Analyzing request and preparing response"", 0.5)
         await super().a_receive(message, sender, request_reply, silent)
 
 
 nest_asyncio.apply()
 
 
 async def main():
-    boss = CustomisedUserProxyAgent(
-        name=""boss"",
-        human_input_mode=""ALWAYS"",
-        max_consecutive_auto_reply=0,
+    print(""🚀 Starting AG2 Async Demo"")
+    print(""="" * 50)
+
+    # Create agents with automated behavior
+    user_proxy = AutomatedUserProxyAgent(
+        name=""hiring_manager"",
+        human_input_mode=""NEVER"",  # No human input required
+        max_consecutive_auto_reply=3,
         code_execution_config=False,
+        is_termination_msg=lambda msg: ""TERMINATE"" in str(msg.get(""content"", """")),
     )
 
-    assistant = CustomisedAssistantAgent(
-        name=""assistant"",
-        system_message=""You will provide some agenda, and I will create questions for an interview meeting. Every time when you generate question then you have to ask user for feedback and if user provides the feedback then you have to incorporate that feedback and generate new set of questions and if user don't want to update then terminate the process and exit"",
+    assistant = AsyncAssistantAgent(
+        name=""interview_consultant"",
+        system_message=""""""You are an expert interview consultant. When given interview topics, 
+        you create thoughtful, relevant questions. You ask for feedback and incorporate it.
+        When the user is satisfied with the questions, end with 'TERMINATE'."""""",
         llm_config={""config_list"": [{""model"": ""gpt-4o-mini"", ""api_key"": os.environ.get(""OPENAI_API_KEY"")}]},
+        is_termination_msg=lambda msg: ""TERMINATE"" in str(msg.get(""content"", """")),
     )
 
-    await boss.a_initiate_chat(
-        assistant,
-        message=""Resume Review, Technical Skills Assessment, Project Discussion, Job Role Expectations, Closing Remarks."",
-        n_results=3,
-    )
-
-
-# await main()
-agentops.end_trace(tracer, end_state=""Success"")
+    try:
+        print(""🤖 Initiating automated conversation..."")
+        await user_proxy.a_initiate_chat(
+            assistant,
+            message=""""""I need help creating interview questions for these topics:
+            - Resume Review
+            - Technical Skills Assessment  
+            - Project Discussion
+            - Job Role Expectations
+            - Closing Remarks
+            
+            Please create 2-3 questions for each topic."""""",
+            max_turns=6,
+        )
+    except Exception as e:
+        print(f""
❌ Error occurred: {e}"")
+    finally:
+        agentops.end_trace(tracer, end_state=""Success"")
+
+    # Validate AgentOps tracking
+    print(""
"" + ""="" * 50)
+    print(""🔍 Validating AgentOps tracking..."")
+    try:
+        agentops.validate_trace_spans(trace_context=tracer)
+        print(""✅ Success! All LLM spans were properly recorded in AgentOps."")
+    except agentops.ValidationError as e:
+        print(f""❌ Error validating spans: {e}"")
+        raise
+
+    print(""
🎉 Demo completed successfully!"")
+
+
+if __name__ == ""__main__"":
+    asyncio.run(main())