@@ -4,20 +4,22 @@
 
 
 def train_crew(n_iterations: int, filename: str) -> None:
-    """"""
-    Train the crew by running a command in the UV environment.
+    """"""Train the crew by running a command in the UV environment.
 
     Args:
         n_iterations (int): The number of iterations to train the crew.
+
     """"""
     command = [""uv"", ""run"", ""train"", str(n_iterations), filename]
 
     try:
         if n_iterations <= 0:
-            raise ValueError(""The number of iterations must be a positive integer."")
+            msg = ""The number of iterations must be a positive integer.""
+            raise ValueError(msg)
 
         if not filename.endswith("".pkl""):
-            raise ValueError(""The filename must not end with .pkl"")
+            msg = ""The filename must not end with .pkl""
+            raise ValueError(msg)
 
         result = subprocess.run(command, capture_output=False, text=True, check=True)
 