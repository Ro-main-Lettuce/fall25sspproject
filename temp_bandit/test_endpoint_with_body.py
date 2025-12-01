@@ -47,7 +47,7 @@ def test_end2end(
     api._register_for_execution(user_proxy)
 
     message = ""Add item with name 'apple', price 1.0""
-    user_proxy.run(
+    user_proxy.initiate_chat(
         agent,
         message=message,
         summary_method=""reflection_with_llm"",