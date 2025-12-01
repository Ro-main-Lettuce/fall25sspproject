@@ -1,10 +1,12 @@
-import pytest
 import re
 from unittest.mock import MagicMock, patch
 
+import pytest
+
 from crewai.agent import Agent
 from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource
 
+
 def test_agent_with_chinese_role_name():
     """"""Test that an agent with a Chinese role name works correctly with the updated regex pattern.""""""
     # Create a knowledge source with some content