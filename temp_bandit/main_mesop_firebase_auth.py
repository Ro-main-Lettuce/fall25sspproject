@@ -48,14 +48,14 @@ def simple_workflow(
         llm_config=llm_config,
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
 
 
 security_policy=me.SecurityPolicy(allowed_iframe_parents=[""https://acme.com""], allowed_script_srcs=[""https://cdn.jsdelivr.net""])