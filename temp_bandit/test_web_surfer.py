@@ -98,18 +98,18 @@ def test_web_surfer_chat_simple_task(
             executor=user_agent,
         )
 
-        run_response = user_agent.run(
+        chat_result = user_agent.initiate_chat(
             assistant_agent,
             message=task,
             summary_method=""reflection_with_llm"",
             max_turns=3,
         )
 
-        assert answer in run_response.summary.lower()
+        assert answer in chat_result.summary.lower()
 
         xs = [
             m[""content""] if m[""content""] is not None else """"
-            for m in run_response.messages
+            for m in chat_result.chat_history
             if m is not None
         ]
         assert any(""We have successfully completed the task"" in m for m in xs)