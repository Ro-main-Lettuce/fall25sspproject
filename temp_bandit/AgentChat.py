@@ -1,5 +1,6 @@
-# Microsoft Autogen Chat Example
+# Microsoft Autogen Multi-Agent Collaboration Example
 #
+# This example demonstrates AI-to-AI collaboration using multiple specialized agents working together without human interaction.
 # AgentOps automatically configures itself when it's initialized meaning your agent run data will be tracked and logged to your AgentOps dashboard right away.
 # First let's install the required packages
 # %pip install -U autogen-agentchat
@@ -9,14 +10,11 @@
 # Then import them
 import os
 from dotenv import load_dotenv
-from IPython.core.error import (
-    StdinNotImplementedError,
-)
 import asyncio
 
 import agentops
 
-from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
+from autogen_agentchat.agents import AssistantAgent
 from autogen_ext.models.openai import OpenAIChatCompletionClient
 
 from autogen_agentchat.teams import RoundRobinGroupChat
@@ -35,9 +33,10 @@
 os.environ[""OPENAI_API_KEY""] = os.getenv(""OPENAI_API_KEY"", ""your_openai_api_key_here"")
 
 # When initializing AgentOps, you can pass in optional tags to help filter sessions
-agentops.init(auto_start_session=False)
+agentops.init(auto_start_session=False, trace_name=""Autogen Multi-Agent Collaboration Example"")
 tracer = agentops.start_trace(
-    trace_name=""Microsoft Agent Chat Example"", tags=[""autogen-chat"", ""microsoft-autogen"", ""agentops-example""]
+    trace_name=""Microsoft Multi-Agent Collaboration Example"",
+    tags=[""autogen-collaboration"", ""microsoft-autogen"", ""agentops-example""],
 )
 
 # AutoGen will now start automatically tracking
@@ -48,50 +47,71 @@
 # * Correspondence between agents
 # * Tool usage
 # * Errors
-# # Simple Chat Example
+# # Multi-Agent Collaboration Example
 # Define model and API key
-model_name = ""gpt-4-turbo""  # Or ""gpt-4o"" / ""gpt-4o-mini"" as per migration guide examples
+model_name = ""gpt-4o-mini""  # Or ""gpt-4o"" / ""gpt-4o-mini"" as per migration guide examples
 api_key = os.getenv(""OPENAI_API_KEY"")
 
 # Create the model client
 model_client = OpenAIChatCompletionClient(model=model_name, api_key=api_key)
 
-# Create the agent that uses the LLM.
-assistant = AssistantAgent(
-    name=""assistant"",
-    system_message=""You are a helpful assistant."",  # Added system message for clarity
+# Create multiple AI agents with different roles
+research_agent = AssistantAgent(
+    name=""research_agent"",
+    system_message=""You are a research specialist. Your role is to gather information, analyze data, and provide insights on topics. You ask thoughtful questions and provide well-researched responses."",
+    model_client=model_client,
+)
+
+creative_agent = AssistantAgent(
+    name=""creative_agent"",
+    system_message=""You are a creative strategist. Your role is to brainstorm innovative solutions, think outside the box, and propose creative approaches to problems. You build on others' ideas and suggest novel perspectives."",
     model_client=model_client,
 )
 
-user_proxy_initiator = UserProxyAgent(""user_initiator"")
+analyst_agent = AssistantAgent(
+    name=""analyst_agent"",
+    system_message=""You are a critical analyst. Your role is to evaluate ideas, identify strengths and weaknesses, and provide constructive feedback. You help refine concepts and ensure practical feasibility."",
+    model_client=model_client,
+)
 
 
 async def main():
-    termination = MaxMessageTermination(max_messages=2)
+    # Set up a longer conversation to allow for meaningful AI-to-AI interaction
+    termination = MaxMessageTermination(max_messages=8)
 
     group_chat = RoundRobinGroupChat(
-        [user_proxy_initiator, assistant],  # Corrected: agents as positional argument
+        [research_agent, creative_agent, analyst_agent],  # AI agents working together
         termination_condition=termination,
     )
 
-    chat_task = ""How can I help you today?""
-    print(f""User Initiator: {chat_task}"")
+    # A task that will engage all three agents in meaningful collaboration
+    chat_task = ""Let's develop a comprehensive strategy for reducing plastic waste in urban environments. I need research on current methods, creative solutions, and analysis of feasibility.""
+    print(f""🎯 Task: {chat_task}"")
+    print(""
"" + ""="" * 80)
+    print(""🤖 AI Agents Collaboration Starting..."")
+    print(""="" * 80)
 
     try:
         stream = group_chat.run_stream(task=chat_task)
-        await Console().run(stream)
+        await Console(stream=stream)
         agentops.end_trace(tracer, end_state=""Success"")
 
-    except StdinNotImplementedError:
-        print(""StdinNotImplementedError: This typically happens in non-interactive environments."")
-        print(""Skipping interactive part of chat for automation."")
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
@@ -109,4 +129,4 @@ async def main():
 
 # You can view data on this run at [app.agentops.ai](app.agentops.ai).
 #
-# The dashboard will display LLM events for each message sent by each agent, including those made by the human user.
+# The dashboard will display LLM events for each message sent by each agent, showing the full AI-to-AI collaboration process with research, creative, and analytical perspectives.