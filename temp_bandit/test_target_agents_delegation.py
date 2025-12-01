@@ -1,10 +1,6 @@
 """"""Test target_agents delegation functionality.""""""
 
-import pytest
 from crewai.agent import Agent
-from crewai.crew import Crew
-from crewai.task import Task
-from crewai.tools.agent_tools.agent_tools import AgentTools
 
 def test_target_agents_filters_delegation_tools():
     """"""Test that target_agents properly filters available agents for delegation.""""""