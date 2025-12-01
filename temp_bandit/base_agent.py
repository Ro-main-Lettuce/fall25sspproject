@@ -315,13 +315,44 @@ def copy(self: T) -> T:  # type: ignore # Signature of ""copy"" incompatible with
         return copied_agent
 
     def _interpolate_only(self, input_string: str, inputs: Dict[str, Any]) -> str:
-        """"""Interpolate placeholders (e.g., {key}) in a string while leaving JSON untouched.""""""
-        escaped_string = input_string.replace(""{"", ""{{"").replace(""}"", ""}}"")
+        """"""Interpolate placeholders in a string while preserving JSON-like structures.
 
-        for key in inputs.keys():
-            escaped_string = escaped_string.replace(f""{{{{{key}}}}}"", f""{{{key}}}"")
+        Args:
+            input_string (str): The string containing placeholders to interpolate.
+            inputs (Dict[str, Any]): Dictionary of values for interpolation.
+
+        Returns:
+            str: The interpolated string with JSON structures preserved.
 
-        return escaped_string.format(**inputs)
+        Example:
+            >>> _interpolate_only(""Name: {name}, Config: {'key': 'value'}"", {""name"": ""John""})
+            ""Name: John, Config: {'key': 'value'}""
+
+        Raises:
+            ValueError: If input_string is None or empty, or if inputs is empty
+            KeyError: If a required template variable is missing from inputs
+        """"""
+        if not input_string:
+            raise ValueError(""Input string cannot be None or empty"")
+        if not inputs:
+            raise ValueError(""Inputs dictionary cannot be empty"")
+
+        try:
+            # First check if all required variables are present
+            required_vars = [
+                var.split(""}"")[0] for var in input_string.split(""{"")[1:]
+                if ""}"" in var
+            ]
+            for var in required_vars:
+                if var not in inputs:
+                    raise KeyError(f""Missing required template variable: {var}"")
+
+            escaped_string = input_string.replace(""{"", ""{{"").replace(""}"", ""}}"")
+            for key in inputs.keys():
+                escaped_string = escaped_string.replace(f""{{{{{key}}}}}"", f""{{{key}}}"")
+            return escaped_string.format(**inputs)
+        except ValueError as e:
+            raise ValueError(f""Error during string interpolation: {str(e)}"") from e
 
     def interpolate_inputs(self, inputs: Dict[str, Any]) -> None:
         """"""Interpolate inputs into the agent description and backstory.""""""