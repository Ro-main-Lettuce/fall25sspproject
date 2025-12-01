@@ -1,15 +1,16 @@
 import os
-import pytest
 import tempfile
-import yaml
 from typing import Type
 
+import pytest
+import yaml
 from pydantic import BaseModel, Field
 
 from crewai import Agent, Crew, Process, Task
 from crewai.project import CrewBase, agent, crew, task, tool
 from crewai.tools import BaseTool
 
+
 def test_function_calling_llm_in_yaml():
     """"""
     Test function_calling_llm YAML configuration.