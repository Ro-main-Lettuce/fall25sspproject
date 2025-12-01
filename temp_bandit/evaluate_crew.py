@@ -4,18 +4,19 @@
 
 
 def evaluate_crew(n_iterations: int, model: str) -> None:
-    """"""
-    Test and Evaluate the crew by running a command in the UV environment.
+    """"""Test and Evaluate the crew by running a command in the UV environment.
 
     Args:
         n_iterations (int): The number of iterations to test the crew.
         model (str): The model to test the crew with.
+
     """"""
     command = [""uv"", ""run"", ""test"", str(n_iterations), model]
 
     try:
         if n_iterations <= 0:
-            raise ValueError(""The number of iterations must be a positive integer."")
+            msg = ""The number of iterations must be a positive integer.""
+            raise ValueError(msg)
 
         result = subprocess.run(command, capture_output=False, text=True, check=True)
 