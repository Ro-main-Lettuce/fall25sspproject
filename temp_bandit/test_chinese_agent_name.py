@@ -1,9 +1,11 @@
-import pytest
 import re
 
+import pytest
+
 from crewai.agent import Agent
 from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource
 
+
 def test_agent_with_chinese_role_name():
     """"""Test that an agent with a Chinese role name works correctly.""""""
     # Create a knowledge source with some content