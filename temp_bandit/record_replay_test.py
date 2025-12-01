@@ -1,6 +1,7 @@
-import pytest
 from unittest.mock import MagicMock, patch
 
+import pytest
+
 from crewai.agent import Agent
 from crewai.crew import Crew
 from crewai.process import Process
@@ -34,8 +35,9 @@ def test_crew_recording_mode():
     mock_llm = MagicMock()
     agent.llm = mock_llm
     
-    with patch('crewai.utilities.llm_response_cache_handler.LLMResponseCacheHandler', return_value=mock_handler):
-        crew.kickoff()
+    with patch('crewai.agent.Agent.execute_task', return_value=""Test response""):
+        with patch('crewai.utilities.llm_response_cache_handler.LLMResponseCacheHandler', return_value=mock_handler):
+            crew.kickoff()
     
     mock_handler.start_recording.assert_called_once()
     
@@ -69,8 +71,9 @@ def test_crew_replay_mode():
     mock_llm = MagicMock()
     agent.llm = mock_llm
     
-    with patch('crewai.utilities.llm_response_cache_handler.LLMResponseCacheHandler', return_value=mock_handler):
-        crew.kickoff()
+    with patch('crewai.agent.Agent.execute_task', return_value=""Test response""):
+        with patch('crewai.utilities.llm_response_cache_handler.LLMResponseCacheHandler', return_value=mock_handler):
+            crew.kickoff()
     
     mock_handler.start_replaying.assert_called_once()
     