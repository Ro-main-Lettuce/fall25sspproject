@@ -1,11 +1,12 @@
-import pytest
 from unittest.mock import MagicMock
 
+import pytest
+
 from crewai.agents.crew_agent_executor import CrewAgentExecutor
 from crewai.agents.parser import (
+    FINAL_ANSWER_AND_PARSABLE_ACTION_ERROR_MESSAGE,
     AgentAction,
     AgentFinish,
-    FINAL_ANSWER_AND_PARSABLE_ACTION_ERROR_MESSAGE,
     OutputParserException,
 )
 