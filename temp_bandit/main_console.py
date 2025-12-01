@@ -40,14 +40,14 @@ def simple_workflow(ui: UI, params: dict[str, Any]) -> str:
         llm_config=llm_config,
     )
 
-    run_response = student_agent.run(
+    chat_result = student_agent.initiate_chat(
         teacher_agent,
         message=initial_message,
         summary_method=""reflection_with_llm"",
         max_turns=5,
     )
 
-    return run_response.summary
+    return chat_result.summary
 
 
 app = FastAgency(provider=wf, ui=ConsoleUI())