@@ -43,7 +43,8 @@ def run_lint():
         raise RuntimeError(f""ruff failed with code {code.returncode}"")
 
 def run_e2e_tests():
-    _run_tests_with_cache(""tests/test_e2e.py"", n_workers=""0"")
+    coloredlogs.install(level=""INFO"")
+    _run_tests_with_cache(""tests/test_e2e.py"", n_workers=""0"", verbose=True)
 
 def generate():
     return Fire(_generate)