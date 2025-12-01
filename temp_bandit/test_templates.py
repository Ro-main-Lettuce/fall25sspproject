@@ -1,7 +1,8 @@
 """"""Test template handling in Agent creation.""""""
 
 import pytest
-from crewai import Agent, Task, Crew
+
+from crewai import Agent, Crew, Task
 
 
 def test_agent_with_only_system_template():