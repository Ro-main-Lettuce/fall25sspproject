@@ -56,14 +56,14 @@ def simple_workflow(ui: UI, params: dict[str, Any]) -> str:
         prompt=""What would you like to find out about weather?"",
     )
 
-    run_response = user_proxy.run(
+    chat_result = user_proxy.initiate_chat(
         weatherman,
         message=initial_message,
         summary_method=""reflection_with_llm"",
         max_turns=3,
     )
 
-    return run_response.summary
+    return chat_result.summary
 
 
 app = FastAgency(provider=wf, ui=ConsoleUI())