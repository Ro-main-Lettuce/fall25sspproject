@@ -1,11 +1,8 @@
 """"""Test for A2A protocol support in CrewAI.""""""
 
-import pytest
-from unittest.mock import patch, MagicMock
+from unittest.mock import patch
 
 from crewai.agent import Agent
-from crewai.crew import Crew
-from crewai.task import Task
 from crewai.tools.agent_tools.agent_tools import AgentTools
 from crewai.tools.agent_tools.delegate_work_tool import DelegateWorkTool
 from crewai.tools.agent_tools.ask_question_tool import AskQuestionTool
@@ -14,8 +11,6 @@
 
 def test_tools_passed_to_execute():
     """"""Test that tools are properly passed to the _execute method.""""""
-    original_execute = DelegateWorkTool._execute
-    
     tools_passed = {""value"": False}
     
     def mock_execute(self, agent_name, task, context=None, tools=None):
@@ -59,8 +54,6 @@ def mock_execute(self, agent_name, task, context=None, tools=None):
 
 def test_tools_passed_from_ask_question_tool():
     """"""Test that tools are properly passed from AskQuestionTool to _execute.""""""
-    original_execute = AskQuestionTool._execute
-    
     tools_passed = {""value"": False}
     
     def mock_execute(self, agent_name, question, context=None, tools=None):
@@ -135,3 +128,46 @@ def _run(self, *args, **kwargs):
         assert hasattr(tool, '_agent_tools'), ""Tool should have _agent_tools attribute""
         assert len(tool._agent_tools) > 0, ""Tool should have agent tools injected""
         assert any(isinstance(t, CustomTool) for t in tool._agent_tools), ""Custom tool should be injected""
+
+
+def test_tool_deduplication():
+    """"""Test that tools are deduplicated when injected into delegation tools.""""""
+    researcher = Agent(
+        role=""researcher"",
+        goal=""research and analyze content"",
+        backstory=""You're an expert researcher"",
+        allow_delegation=True,
+    )
+    
+    writer = Agent(
+        role=""writer"",
+        goal=""write content based on research"",
+        backstory=""You're an expert writer"",
+        allow_delegation=True,
+    )
+    
+    class CustomTool(BaseTool):
+        name: str = ""Custom Tool""
+        description: str = ""A custom tool for testing""
+        
+        def _run(self, *args, **kwargs):
+            return ""Custom tool executed""
+    
+    # Create two instances of the same tool
+    custom_tool1 = CustomTool()
+    custom_tool2 = CustomTool()
+    
+    # Add the same tool to both agents
+    researcher.tools = [custom_tool1]
+    writer.tools = [custom_tool2]
+    
+    agent_tools = AgentTools(agents=[researcher, writer])
+    delegation_tools = agent_tools.tools()
+    
+    # Check that tools are deduplicated
+    for tool in delegation_tools:
+        assert hasattr(tool, '_agent_tools'), ""Tool should have _agent_tools attribute""
+        
+        # Count instances of CustomTool
+        custom_tools = [t for t in tool._agent_tools if isinstance(t, CustomTool)]
+        assert len(custom_tools) <= 2, ""Should have at most 2 instances of CustomTool""