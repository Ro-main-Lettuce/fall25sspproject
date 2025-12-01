@@ -1,4 +1,3 @@
-import asyncio
 from typing import cast
 from unittest.mock import Mock
 
@@ -35,10 +34,9 @@ def _run(self, query: str) -> str:
         # This is a mock implementation
         if ""tokyo"" in query.lower():
             return ""Tokyo's population in 2023 was approximately 21 million people in the city proper, and 37 million in the greater metropolitan area.""
-        elif ""climate change"" in query.lower() and ""coral"" in query.lower():
+        if ""climate change"" in query.lower() and ""coral"" in query.lower():
             return ""Climate change severely impacts coral reefs through: 1) Ocean warming causing coral bleaching, 2) Ocean acidification reducing calcification, 3) Sea level rise affecting light availability, 4) Increased storm frequency damaging reef structures. Sources: NOAA Coral Reef Conservation Program, Global Coral Reef Alliance.""
-        else:
-            return f""Found information about {query}: This is a simulated search result for demonstration purposes.""
+        return f""Found information about {query}: This is a simulated search result for demonstration purposes.""
 
 
 # Define Mock Calculator Tool
@@ -54,7 +52,7 @@ def _run(self, expression: str) -> str:
             result = eval(expression, {""__builtins__"": {}})
             return f""The result of {expression} is {result}""
         except Exception as e:
-            return f""Error calculating {expression}: {str(e)}""
+            return f""Error calculating {expression}: {e!s}""
 
 
 # Define a custom response format using Pydantic
@@ -68,7 +66,7 @@ class ResearchResult(BaseModel):
 
 @pytest.mark.vcr(filter_headers=[""authorization""])
 @pytest.mark.parametrize(""verbose"", [True, False])
-def test_lite_agent_created_with_correct_parameters(monkeypatch, verbose):
+def test_lite_agent_created_with_correct_parameters(monkeypatch, verbose) -> None:
     """"""Test that LiteAgent is created with the correct parameters when Agent.kickoff() is called.""""""
     # Create a test agent with specific parameters
     llm = LLM(model=""gpt-4o-mini"")
@@ -93,7 +91,7 @@ def test_lite_agent_created_with_correct_parameters(monkeypatch, verbose):
 
     # Define a mock LiteAgent class that captures its arguments
     class MockLiteAgent(original_lite_agent):
-        def __init__(self, **kwargs):
+        def __init__(self, **kwargs) -> None:
             nonlocal created_lite_agent
             created_lite_agent = kwargs
             super().__init__(**kwargs)
@@ -129,7 +127,7 @@ class TestResponse(BaseModel):
 
 
 @pytest.mark.vcr(filter_headers=[""authorization""])
-def test_lite_agent_with_tools():
+def test_lite_agent_with_tools() -> None:
     """"""Test that Agent can use tools.""""""
     # Create a LiteAgent with tools
     llm = LLM(model=""gpt-4o-mini"")
@@ -143,7 +141,7 @@ def test_lite_agent_with_tools():
     )
 
     result = agent.kickoff(
-        ""What is the population of Tokyo and how many people would that be per square kilometer if Tokyo's area is 2,194 square kilometers?""
+        ""What is the population of Tokyo and how many people would that be per square kilometer if Tokyo's area is 2,194 square kilometers?"",
     )
 
     assert (
@@ -156,7 +154,7 @@ def test_lite_agent_with_tools():
     received_events = []
 
     @crewai_event_bus.on(ToolUsageStartedEvent)
-    def event_handler(source, event):
+    def event_handler(source, event) -> None:
         received_events.append(event)
 
     agent.kickoff(""What are the effects of climate change on coral reefs?"")
@@ -196,13 +194,10 @@ class SimpleOutput(BaseModel):
         response_format=SimpleOutput,
     )
 
-    print(f""
=== Agent Result Type: {type(result)}"")
-    print(f""=== Agent Result: {result}"")
-    print(f""=== Pydantic: {result.pydantic}"")
 
     assert result.pydantic is not None, ""Should return a Pydantic model""
 
-    output = cast(SimpleOutput, result.pydantic)
+    output = cast(""SimpleOutput"", result.pydantic)
 
     assert isinstance(output.summary, str), ""Summary should be a string""
     assert len(output.summary) > 0, ""Summary should not be empty""
@@ -217,7 +212,7 @@ class SimpleOutput(BaseModel):
 
 
 @pytest.mark.vcr(filter_headers=[""authorization""])
-def test_lite_agent_returns_usage_metrics():
+def test_lite_agent_returns_usage_metrics() -> None:
     """"""Test that LiteAgent returns usage metrics.""""""
     llm = LLM(model=""gpt-4o-mini"")
     agent = Agent(
@@ -230,7 +225,7 @@ def test_lite_agent_returns_usage_metrics():
     )
 
     result = agent.kickoff(
-        ""What is the population of Tokyo? Return your strucutred output in JSON format with the following fields: summary, confidence""
+        ""What is the population of Tokyo? Return your strucutred output in JSON format with the following fields: summary, confidence"",
     )
 
     assert result.usage_metrics is not None
@@ -239,7 +234,7 @@ def test_lite_agent_returns_usage_metrics():
 
 @pytest.mark.vcr(filter_headers=[""authorization""])
 @pytest.mark.asyncio
-async def test_lite_agent_returns_usage_metrics_async():
+async def test_lite_agent_returns_usage_metrics_async() -> None:
     """"""Test that LiteAgent returns usage metrics when run asynchronously.""""""
     llm = LLM(model=""gpt-4o-mini"")
     agent = Agent(
@@ -252,7 +247,7 @@ async def test_lite_agent_returns_usage_metrics_async():
     )
 
     result = await agent.kickoff_async(
-        ""What is the population of Tokyo? Return your strucutred output in JSON format with the following fields: summary, confidence""
+        ""What is the population of Tokyo? Return your strucutred output in JSON format with the following fields: summary, confidence"",
     )
     assert isinstance(result, LiteAgentOutput)
     assert ""21 million"" in result.raw or ""37 million"" in result.raw
@@ -263,7 +258,7 @@ async def test_lite_agent_returns_usage_metrics_async():
 class TestFlow(Flow):
     """"""A test flow that creates and runs an agent.""""""
 
-    def __init__(self, llm, tools):
+    def __init__(self, llm, tools) -> None:
         self.llm = llm
         self.tools = tools
         super().__init__()
@@ -280,14 +275,14 @@ def start(self):
         return agent.kickoff(""Test query"")
 
 
-def verify_agent_parent_flow(result, agent, flow):
+def verify_agent_parent_flow(result, agent, flow) -> None:
     """"""Verify that both the result and agent have the correct parent flow.""""""
     assert result.parent_flow is flow
     assert agent is not None
     assert agent.parent_flow is flow
 
 
-def test_sets_parent_flow_when_inside_flow():
+def test_sets_parent_flow_when_inside_flow() -> None:
     captured_agent = None
 
     mock_llm = Mock(spec=LLM)
@@ -309,9 +304,9 @@ def start(self):
     with crewai_event_bus.scoped_handlers():
 
         @crewai_event_bus.on(LiteAgentExecutionStartedEvent)
-        def capture_agent(source, event):
+        def capture_agent(source, event) -> None:
             nonlocal captured_agent
             captured_agent = source
 
-        result = flow.kickoff()
+        flow.kickoff()
         assert captured_agent.parent_flow is flow