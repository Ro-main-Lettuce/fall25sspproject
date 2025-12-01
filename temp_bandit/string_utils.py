@@ -1,10 +1,10 @@
 import re
-from typing import Any, Dict, List, Optional, Union
+from typing import Any
 
 
 def interpolate_only(
-    input_string: Optional[str],
-    inputs: Dict[str, Union[str, int, float, Dict[str, Any], List[Any]]],
+    input_string: str | None,
+    inputs: dict[str, str | int | float | dict[str, Any] | list[Any]],
 ) -> str:
     """"""Interpolate placeholders (e.g., {key}) in a string while leaving JSON untouched.
     Only interpolates placeholders that follow the pattern {variable_name} where
@@ -23,6 +23,7 @@ def interpolate_only(
 
     Raises:
         ValueError: If a value contains unsupported types or a template variable is missing
+
     """"""
 
     # Validation function for recursive type checking
@@ -35,25 +36,30 @@ def validate_type(value: Any) -> None:
             for item in value.values() if isinstance(value, dict) else value:
                 validate_type(item)
             return
-        raise ValueError(
+        msg = (
             f""Unsupported type {type(value).__name__} in inputs. ""
             ""Only str, int, float, bool, dict, and list are allowed.""
         )
+        raise ValueError(
+            msg,
+        )
 
     # Validate all input values
     for key, value in inputs.items():
         try:
             validate_type(value)
         except ValueError as e:
-            raise ValueError(f""Invalid value for key '{key}': {str(e)}"") from e
+            msg = f""Invalid value for key '{key}': {e!s}""
+            raise ValueError(msg) from e
 
     if input_string is None or not input_string:
         return """"
     if ""{"" not in input_string and ""}"" not in input_string:
         return input_string
     if not inputs:
+        msg = ""Inputs dictionary cannot be empty when interpolating variables""
         raise ValueError(
-            ""Inputs dictionary cannot be empty when interpolating variables""
+            msg,
         )
 
     # The regex pattern to find valid variable placeholders
@@ -68,8 +74,9 @@ def validate_type(value: Any) -> None:
     # Check if all variables exist in inputs
     missing_vars = [var for var in variables if var not in inputs]
     if missing_vars:
+        msg = f""Template variable '{missing_vars[0]}' not found in inputs dictionary""
         raise KeyError(
-            f""Template variable '{missing_vars[0]}' not found in inputs dictionary""
+            msg,
         )
 
     # Replace each variable with its value