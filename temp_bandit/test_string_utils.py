@@ -1,4 +1,4 @@
-from typing import Any, Dict, List, Union
+from typing import Any
 
 import pytest
 
@@ -8,10 +8,10 @@
 class TestInterpolateOnly:
     """"""Tests for the interpolate_only function in string_utils.py.""""""
 
-    def test_basic_variable_interpolation(self):
+    def test_basic_variable_interpolation(self) -> None:
         """"""Test basic variable interpolation works correctly.""""""
         template = ""Hello, {name}! Welcome to {company}.""
-        inputs: Dict[str, Union[str, int, float, Dict[str, Any], List[Any]]] = {
+        inputs: dict[str, str | int | float | dict[str, Any] | list[Any]] = {
             ""name"": ""Alice"",
             ""company"": ""CrewAI"",
         }
@@ -20,18 +20,18 @@ def test_basic_variable_interpolation(self):
 
         assert result == ""Hello, Alice! Welcome to CrewAI.""
 
-    def test_multiple_occurrences_of_same_variable(self):
+    def test_multiple_occurrences_of_same_variable(self) -> None:
         """"""Test that multiple occurrences of the same variable are replaced.""""""
         template = ""{name} is using {name}'s account.""
-        inputs: Dict[str, Union[str, int, float, Dict[str, Any], List[Any]]] = {
-            ""name"": ""Bob""
+        inputs: dict[str, str | int | float | dict[str, Any] | list[Any]] = {
+            ""name"": ""Bob"",
         }
 
         result = interpolate_only(template, inputs)
 
         assert result == ""Bob is using Bob's account.""
 
-    def test_json_structure_preservation(self):
+    def test_json_structure_preservation(self) -> None:
         """"""Test that JSON structures are preserved and not interpolated incorrectly.""""""
         template = """"""
         Instructions for {agent}:
@@ -40,8 +40,8 @@ def test_json_structure_preservation(self):
 
         {""name"": ""person's name"", ""age"": 25, ""skills"": [""coding"", ""testing""]}
         """"""
-        inputs: Dict[str, Union[str, int, float, Dict[str, Any], List[Any]]] = {
-            ""agent"": ""DevAgent""
+        inputs: dict[str, str | int | float | dict[str, Any] | list[Any]] = {
+            ""agent"": ""DevAgent"",
         }
 
         result = interpolate_only(template, inputs)
@@ -52,7 +52,7 @@ def test_json_structure_preservation(self):
             in result
         )
 
-    def test_complex_nested_json(self):
+    def test_complex_nested_json(self) -> None:
         """"""Test with complex JSON structures containing curly braces.""""""
         template = """"""
         {agent} needs to process:
@@ -65,8 +65,8 @@ def test_complex_nested_json(self):
           }
         }
         """"""
-        inputs: Dict[str, Union[str, int, float, Dict[str, Any], List[Any]]] = {
-            ""agent"": ""DataProcessor""
+        inputs: dict[str, str | int | float | dict[str, Any] | list[Any]] = {
+            ""agent"": ""DataProcessor"",
         }
 
         result = interpolate_only(template, inputs)
@@ -76,11 +76,11 @@ def test_complex_nested_json(self):
         assert '""value"": 42' in result
         assert '[1, 2, {""inner"": ""value""}]' in result
 
-    def test_missing_variable(self):
+    def test_missing_variable(self) -> None:
         """"""Test that an error is raised when a required variable is missing.""""""
         template = ""Hello, {name}!""
-        inputs: Dict[str, Union[str, int, float, Dict[str, Any], List[Any]]] = {
-            ""not_name"": ""Alice""
+        inputs: dict[str, str | int | float | dict[str, Any] | list[Any]] = {
+            ""not_name"": ""Alice"",
         }
 
         with pytest.raises(KeyError) as excinfo:
@@ -89,55 +89,55 @@ def test_missing_variable(self):
         assert ""template variable"" in str(excinfo.value).lower()
         assert ""name"" in str(excinfo.value)
 
-    def test_invalid_input_types(self):
+    def test_invalid_input_types(self) -> None:
         """"""Test that an error is raised with invalid input types.""""""
         template = ""Hello, {name}!""
         # Using Any for this test since we're intentionally testing an invalid type
-        inputs: Dict[str, Any] = {""name"": object()}  # Object is not a valid input type
+        inputs: dict[str, Any] = {""name"": object()}  # Object is not a valid input type
 
         with pytest.raises(ValueError) as excinfo:
             interpolate_only(template, inputs)
 
         assert ""unsupported type"" in str(excinfo.value).lower()
 
-    def test_empty_input_string(self):
+    def test_empty_input_string(self) -> None:
         """"""Test handling of empty or None input string.""""""
-        inputs: Dict[str, Union[str, int, float, Dict[str, Any], List[Any]]] = {
-            ""name"": ""Alice""
+        inputs: dict[str, str | int | float | dict[str, Any] | list[Any]] = {
+            ""name"": ""Alice"",
         }
 
         assert interpolate_only("""", inputs) == """"
         assert interpolate_only(None, inputs) == """"
 
-    def test_no_variables_in_template(self):
+    def test_no_variables_in_template(self) -> None:
         """"""Test a template with no variables to replace.""""""
         template = ""This is a static string with no variables.""
-        inputs: Dict[str, Union[str, int, float, Dict[str, Any], List[Any]]] = {
-            ""name"": ""Alice""
+        inputs: dict[str, str | int | float | dict[str, Any] | list[Any]] = {
+            ""name"": ""Alice"",
         }
 
         result = interpolate_only(template, inputs)
 
         assert result == template
 
-    def test_variable_name_starting_with_underscore(self):
+    def test_variable_name_starting_with_underscore(self) -> None:
         """"""Test variables starting with underscore are replaced correctly.""""""
         template = ""Variable: {_special_var}""
-        inputs: Dict[str, Union[str, int, float, Dict[str, Any], List[Any]]] = {
-            ""_special_var"": ""Special Value""
+        inputs: dict[str, str | int | float | dict[str, Any] | list[Any]] = {
+            ""_special_var"": ""Special Value"",
         }
 
         result = interpolate_only(template, inputs)
 
         assert result == ""Variable: Special Value""
 
-    def test_preserves_non_matching_braces(self):
+    def test_preserves_non_matching_braces(self) -> None:
         """"""Test that non-matching braces patterns are preserved.""""""
         template = (
             ""This {123} and {!var} should not be replaced but {valid_var} should.""
         )
-        inputs: Dict[str, Union[str, int, float, Dict[str, Any], List[Any]]] = {
-            ""valid_var"": ""works""
+        inputs: dict[str, str | int | float | dict[str, Any] | list[Any]] = {
+            ""valid_var"": ""works"",
         }
 
         result = interpolate_only(template, inputs)
@@ -146,15 +146,15 @@ def test_preserves_non_matching_braces(self):
             result == ""This {123} and {!var} should not be replaced but works should.""
         )
 
-    def test_complex_mixed_scenario(self):
+    def test_complex_mixed_scenario(self) -> None:
         """"""Test a complex scenario with both valid variables and JSON structures.""""""
         template = """"""
         {agent_name} is working on task {task_id}.
-        
+
         Instructions:
         1. Process the data
         2. Return results as:
-        
+
         {
           ""taskId"": ""{task_id}"",
           ""results"": {
@@ -164,7 +164,7 @@ def test_complex_mixed_scenario(self):
           }
         }
         """"""
-        inputs: Dict[str, Union[str, int, float, Dict[str, Any], List[Any]]] = {
+        inputs: dict[str, str | int | float | dict[str, Any] | list[Any]] = {
             ""agent_name"": ""AnalyticsAgent"",
             ""task_id"": ""T-12345"",
         }
@@ -176,10 +176,10 @@ def test_complex_mixed_scenario(self):
         assert '""processed_by"": ""agent_name""' in result  # This shouldn't be replaced
         assert '""values"": [1, 2, 3]' in result
 
-    def test_empty_inputs_dictionary(self):
+    def test_empty_inputs_dictionary(self) -> None:
         """"""Test that an error is raised with empty inputs dictionary.""""""
         template = ""Hello, {name}!""
-        inputs: Dict[str, Any] = {}
+        inputs: dict[str, Any] = {}
 
         with pytest.raises(ValueError) as excinfo:
             interpolate_only(template, inputs)