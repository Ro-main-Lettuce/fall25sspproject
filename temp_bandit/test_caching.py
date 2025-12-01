@@ -13,7 +13,7 @@ def test_same_value_caching(tmp_path):
     for _ in range(3):
 
         def prompt_func():
-            return f""Say '1'. Do not explain.""
+            return ""Say '1'. Do not explain.""
 
         prompter = curator.LLM(
             prompt_func=prompt_func,
@@ -34,8 +34,10 @@ def test_different_values_caching(tmp_path):
 
     # Test with different values
     for x in [1, 2, 3]:
+        # Bind x to avoid late binding closure issue
+        x_val = x
 
-        def prompt_func():
+        def prompt_func(x=x_val):
             return f""Say '{x}'. Do not explain.""
 
         prompter = curator.LLM(
@@ -106,7 +108,7 @@ def prompt_func():
     result = prompter(working_dir=str(tmp_path))
     assert result.to_pandas().iloc[0][""response""] == ""1""
 
-    def value_generator():
+    def value_generator():  # noqa: F811
         return 2
 
     result = prompter(working_dir=str(tmp_path))
@@ -182,18 +184,14 @@ def prompt_func(x):
 def test_function_hash_dir_change():
     """"""Test that identical functions in different directories but same base filename produce the same hash.""""""
     import logging
-    import os
-    import sys
     import tempfile
     from pathlib import Path
 
     from bespokelabs.curator.llm.llm import _get_function_hash
 
     # Set up logging to write to a file in the current directory
     debug_log = Path(""function_debug.log"")
-    logging.basicConfig(
-        level=logging.DEBUG, format=""%(message)s"", filename=str(debug_log), filemode=""w""
-    )
+    logging.basicConfig(level=logging.DEBUG, format=""%(message)s"", filename=str(debug_log), filemode=""w"")
     logger = logging.getLogger(__name__)
 
     def dump_function_details(func, prefix):
@@ -261,10 +259,10 @@ def test_func():
         # Both should produce the same hash
         hash1 = _get_function_hash(func1)
         hash2 = _get_function_hash(func2)
-        print(f""
Hash comparison:"")  # Print to stdout
+        print(""
Hash comparison:"")  # Print to stdout
         print(f""  hash1: {hash1}"")
         print(f""  hash2: {hash2}"")
-        logger.debug(f""
Hash comparison:"")
+        logger.debug(""
Hash comparison:"")
         logger.debug(f""  hash1: {hash1}"")
         logger.debug(f""  hash2: {hash2}"")
 