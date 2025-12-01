@@ -1,8 +1,7 @@
-import pytest
 from unittest.mock import Mock, patch
-from crewai import Agent, Task, LLM
+from crewai import Agent, LLM
 from crewai.tasks.task_output import TaskOutput
-from crewai.lite_agent import LiteAgent, LiteAgentOutput
+from crewai.lite_agent import LiteAgentOutput
 from crewai.utilities.xml_parser import (
     extract_xml_content,
     extract_all_xml_content,
@@ -202,7 +201,7 @@ def test_remove_xml_tags(self):
         """"""Test removing XML tags and their content.""""""
         text = ""Keep this <thinking>Remove this</thinking> and this""
         result = remove_xml_tags(text, [""thinking""])
-        assert result == ""Keep this and this""
+        assert result == ""Keep this  and this""
 
     def test_strip_xml_tags_keep_content(self):
         """"""Test stripping XML tags but keeping content.""""""