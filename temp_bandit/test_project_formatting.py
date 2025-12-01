@@ -30,69 +30,12 @@ def test_project_formatting(temp_dir):
         # Fix imports in the generated project's main.py file
         main_py_path = Path(temp_dir) / ""test_crew"" / ""src"" / ""test_crew"" / ""main.py""
         
-        # Directly fix the imports in the file
-        # This is a simpler approach that should work in all environments
-        with open(main_py_path, ""w"") as f:
-            f.write(""""""#!/usr/bin/env python
-import sys
-import warnings
-from datetime import datetime
-
-from test_crew.crew import TestCrew
-
-warnings.filterwarnings(""ignore"", category=SyntaxWarning, module=""pysbd"")
-
-# This main file is intended to be a way for you to run your
-# crew locally, so refrain from adding unnecessary logic into this file.
-# Replace with inputs you want to test with, it will automatically
-# interpolate any tasks and agents information
-
-def run():
-    """"""
-    Run the crew.
-    """"""
-    inputs = {
-        'topic': 'AI LLMs'
-    }
-    TestCrew().crew().kickoff(inputs=inputs)
-
-
-def train():
-    """"""
-    Train the crew for a given number of iterations.
-    """"""
-    inputs = {
-        ""topic"": ""AI LLMs""
-    }
-    try:
-        TestCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
-
-    except Exception as e:
-        raise Exception(f""An error occurred while training the crew: {e}"")
-
-def replay():
-    """"""
-    Replay the crew execution from a specific task.
-    """"""
-    try:
-        TestCrew().crew().replay(task_id=sys.argv[1])
-
-    except Exception as e:
-        raise Exception(f""An error occurred while replaying the crew: {e}"")
-
-def test():
-    """"""
-    Test the crew execution and returns the results.
-    """"""
-    inputs = {
-        ""topic"": ""AI LLMs""
-    }
-    try:
-        TestCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)
-
-    except Exception as e:
-        raise Exception(f""An error occurred while replaying the crew: {e}"")
-"""""")
+        # Use ruff to fix the imports
+        subprocess.run(
+            [""ruff"", ""check"", ""--select=I"", ""--fix"", str(main_py_path)],
+            capture_output=True,
+            text=True,
+        )
 
         # Create a ruff configuration file
         ruff_config = """"""