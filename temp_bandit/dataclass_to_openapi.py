@@ -52,6 +52,10 @@ def convert(
         origin = get_origin(py_type)
         optional_name_overrides = self.optional_name_overrides
 
+        # Handle NewType by unwrapping to its base type
+        if hasattr(py_type, ""__supertype__""):  # NewType check
+            return self.convert(py_type.__supertype__, processed_classes)
+
         if origin is Union:
             args = get_args(py_type)
 