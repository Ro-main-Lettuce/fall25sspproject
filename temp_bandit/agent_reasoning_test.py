@@ -170,7 +170,6 @@ def test_agent_reasoning_error_handling():
         agent=agent
     )
     
-    original_call = agent.llm.call
     call_count = [0]
     
     def mock_llm_call_error(*args, **kwargs):