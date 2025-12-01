@@ -1,36 +1,44 @@
-# Agent Chat with Async Operations
+# AG2 Async Agent Chat with Automated Responses
 #
-# We are going to create agents that can perform asynchronous operations and chat with each other.
-# This example demonstrates async capabilities without requiring human input.
+# This notebook demonstrates how to leverage asynchronous programming with AG2 agents 
+# to create automated conversations between AI agents, eliminating the need for human 
+# input while maintaining full traceability.
 #
-# We are going to use AgentOps to monitor the agent's performance and observe their interactions.
-# # Install required dependencies
+# Overview
+# This notebook demonstrates a practical example of automated AI-to-AI communication where we:
+#
+# 1. Initialize AG2 agents with OpenAI's GPT-4o-mini model
+# 2. Create custom async agents that simulate human-like responses and processing delays
+# 3. Automate the entire conversation flow without requiring manual intervention
+# 4. Track all interactions using AgentOps for monitoring and analysis
+#
+# By using async operations and automated responses, you can create fully autonomous 
+# agent conversations that simulate real-world scenarios. This is particularly useful 
+# for testing, prototyping, and creating demos where you want to showcase agent 
+# capabilities without manual input.
+
 # %pip install agentops
 # %pip install ag2
-# %pip install chromadb
-# %pip install sentence_transformers
-# %pip install tiktoken
-# %pip install pypdf
 # %pip install nest-asyncio
+
 import asyncio
 from typing import Dict, Optional, Union
 import os
 from dotenv import load_dotenv
-
 import nest_asyncio
 import agentops
 from autogen import AssistantAgent
 from autogen.agentchat.user_proxy_agent import UserProxyAgent
 
+# Load environment variables for API keys
 load_dotenv()
 os.environ[""AGENTOPS_API_KEY""] = os.getenv(""AGENTOPS_API_KEY"", ""your_api_key_here"")
 os.environ[""OPENAI_API_KEY""] = os.getenv(""OPENAI_API_KEY"", ""your_openai_api_key_here"")
-
+# Initialize AgentOps for tracking and monitoring
 agentops.init(auto_start_session=False, trace_name=""AG2 Async Demo"")
 tracer = agentops.start_trace(trace_name=""AG2 Async Agent Demo"", tags=[""ag2-async-demo"", ""agentops-example""])
 
-
-# Define an asynchronous function that simulates async processing
+# Define an asynchronous function that simulates async processing 
 async def simulate_async_processing(task_name: str, delay: float = 1.0) -> str:
     """"""
     Simulate some asynchronous processing (e.g., API calls, file operations, etc.)
@@ -40,8 +48,7 @@ async def simulate_async_processing(task_name: str, delay: float = 1.0) -> str:
     print(f""✅ Completed async task: {task_name}"")
     return f""Processed: {task_name}""
 
-
-# Define a custom UserProxyAgent that simulates automated responses
+# Define a custom UserProxyAgent that simulates automated user responses
 class AutomatedUserProxyAgent(UserProxyAgent):
     def __init__(self, name: str, **kwargs):
         super().__init__(name, **kwargs)
@@ -74,7 +81,7 @@ async def a_receive(
     ):
         await super().a_receive(message, sender, request_reply, silent)
 
-
+# Define an AssistantAgent that simulates async processing before responding
 class AsyncAssistantAgent(AssistantAgent):
     async def a_receive(
         self,
@@ -88,12 +95,8 @@ async def a_receive(
         await super().a_receive(message, sender, request_reply, silent)
 
 
-nest_asyncio.apply()
-
-
 async def main():
     print(""🚀 Starting AG2 Async Demo"")
-    print(""="" * 50)
 
     # Create agents with automated behavior
     user_proxy = AutomatedUserProxyAgent(
@@ -115,6 +118,7 @@ async def main():
 
     try:
         print(""🤖 Initiating automated conversation..."")
+        # Start the automated chat between the user and assistant
         await user_proxy.a_initiate_chat(
             assistant,
             message=""""""I need help creating interview questions for these topics:
@@ -127,23 +131,25 @@ async def main():
             Please create 2-3 questions for each topic."""""",
             max_turns=6,
         )
+
+        # Let's check programmatically that spans were recorded in AgentOps
+        print(""
"" + ""="" * 50)
+        print(""Now let's verify that our LLM calls were tracked properly..."")
+        try:
+            agentops.validate_trace_spans(trace_context=tracer)
+            print(""
✅ Success! All LLM spans were properly recorded in AgentOps."")
+        except agentops.ValidationError as e:
+            print(f""
❌ Error validating spans: {e}"")
+            raise
+
     except Exception as e:
         print(f""
❌ Error occurred: {e}"")
     finally:
         agentops.end_trace(tracer, end_state=""Success"")
 
-    # Validate AgentOps tracking
-    print(""
"" + ""="" * 50)
-    print(""🔍 Validating AgentOps tracking..."")
-    try:
-        agentops.validate_trace_spans(trace_context=tracer)
-        print(""✅ Success! All LLM spans were properly recorded in AgentOps."")
-    except agentops.ValidationError as e:
-        print(f""❌ Error validating spans: {e}"")
-        raise
-
     print(""
🎉 Demo completed successfully!"")
 
+# Run the main async demo
+nest_asyncio.apply()
+asyncio.run(main())
 
-if __name__ == ""__main__"":
-    asyncio.run(main())