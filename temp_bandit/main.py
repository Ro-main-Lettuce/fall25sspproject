@@ -33,7 +33,8 @@ def train():
     Train the crew for a given number of iterations.
     """"""
     inputs = {
-        ""topic"": ""AI LLMs""
+        ""topic"": ""AI LLMs"",
+        'current_year': str(datetime.now().year)
     }
     try:
         {{crew_name}}().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
@@ -59,6 +60,7 @@ def test():
         ""topic"": ""AI LLMs"",
         ""current_year"": str(datetime.now().year)
     }
+    
     try:
         {{crew_name}}().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)
 