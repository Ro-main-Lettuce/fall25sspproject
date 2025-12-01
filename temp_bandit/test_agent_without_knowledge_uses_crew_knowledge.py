@@ -1,7 +1,8 @@
-import pytest
 from unittest.mock import MagicMock, patch
 
-from crewai import Agent, Crew, LLM, Process, Task
+import pytest
+
+from crewai import LLM, Agent, Crew, Process, Task
 from crewai.knowledge.knowledge import Knowledge
 from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource
 