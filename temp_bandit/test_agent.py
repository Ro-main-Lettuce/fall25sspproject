@@ -1,10 +1,12 @@
 import os
-import pytest
 from unittest import mock
 
+import pytest
+
 from crewai.agent import Agent
 from crewai.llm import LLM
 
+
 def test_agent_with_custom_llm():
     """"""Test creating an agent with a custom LLM.""""""
     custom_llm = LLM(model=""gpt-4"")