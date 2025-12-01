@@ -227,7 +227,7 @@ def test_end2end(
     api._register_for_llm(agent)
     api._register_for_execution(user_proxy)
 
-    result = user_proxy.run(
+    result = user_proxy.initiate_chat(
         agent,
         message=""I need the 'url' for gif with id 1"",
         summary_method=""reflection_with_llm"",
@@ -236,7 +236,7 @@ def test_end2end(
 
     assert ""https://gif.example.com/gif1"" in result.summary
 
-    user_proxy.run(
+    user_proxy.initiate_chat(
         agent,
         message=""I need the urls all gifs for 'topic' 'funny'. Within the summary, please include the 'url' for each gif."",
         summary_method=""reflection_with_llm"",