@@ -129,14 +129,14 @@ def simple_workflow(ui: UI, params: dict[str, Any]) -> str:
         # human_input_mode=""ALWAYS"",
     )
 
-    run_response = student_agent.run(
+    chat_result = student_agent.initiate_chat(
         teacher_agent,
         message=initial_message,
         summary_method=""reflection_with_llm"",
         max_turns=5,
     )
 
-    return run_response.summary  # type: ignore[no-any-return]
+    return chat_result.summary  # type: ignore[no-any-return]
 
 adapter = FastAPIAdapter(provider=wf)
 