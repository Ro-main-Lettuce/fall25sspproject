@@ -36,6 +36,10 @@ def preprocess_future_imports(code: str) -> str:
     This ensures that future imports are always at the top of the file,
     which is required by Python's compiler.
     """"""
+    # Quick check if __future__ is even in the code
+    if ""__future__"" not in code:
+        return code
+
     # Check if the code already starts with a future import
     if code.lstrip().startswith(""from __future__""):
         return code