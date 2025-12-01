@@ -57,14 +57,14 @@ def is_termination_msg(msg: dict[str, Any]) -> bool:
         executor=user_agent,
     )
 
-    run_response = user_agent.run(
+    chat_result = user_agent.initiate_chat(
         assistant_agent,
         message=initial_message,
         summary_method=""reflection_with_llm"",
         max_turns=5,
     )
 
-    return run_response.summary  # type: ignore[no-any-return]
+    return chat_result.summary  # type: ignore[no-any-return]
 
 
 app = FastAgency(provider=wf, ui=ConsoleUI())