@@ -133,7 +133,9 @@ def test_agent_fallback_context_window_error():
     with patch.object(primary_llm, 'call') as mock_primary, \
          patch.object(fallback_llm, 'call') as mock_fallback:
         
-        mock_primary.side_effect = ContextWindowExceededError(""Context window exceeded"")
+        mock_primary.side_effect = ContextWindowExceededError(
+            message=""Context window exceeded"", model=""gpt-4"", llm_provider=""openai""
+        )
         mock_fallback.return_value = ""Fallback response""
         
         result = agent.execute_task(task)