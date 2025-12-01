@@ -66,14 +66,14 @@ def is_termination_msg(msg: dict[str, Any]) -> bool:
         prompt=""I can help you find images related to a certain subject. What kind of images would you like to find?"",
     )
 
-    run_response = user_proxy.run(
+    chat_result = user_proxy.initiate_chat(
         giphy_agent,
         message=initial_message,
         summary_method=""reflection_with_llm"",
         max_turns=10,
     )
 
-    return run_response.summary  # type: ignore[no-any-return]
+    return chat_result.summary  # type: ignore[no-any-return]
 
 
 app = FastAgency(provider=wf, ui=MesopUI(), title=""Giphy chat"")