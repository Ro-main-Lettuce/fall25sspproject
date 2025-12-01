@@ -65,14 +65,14 @@ def weather_workflow_with_security(
         executors=weather_agent,
     )
 
-    run_response = user_agent.run(
+    chat_result = user_agent.initiate_chat(
         weather_agent,
         message=initial_message,
         summary_method=""reflection_with_llm"",
         max_turns=3,
     )
 
-    return run_response.summary  # type: ignore[no-any-return]
+    return chat_result.summary  # type: ignore[no-any-return]
 
 
 app = FastAgency(provider=wf, ui=ConsoleUI())