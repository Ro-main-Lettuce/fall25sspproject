@@ -51,30 +51,16 @@ def test_custom_openai_json_conversion_with_instructor_error(self, mock_llm_with
             # Verify that the fallback mechanism was used
             mock_llm_with_function_calling.call.assert_called_once()
             
-            # The result should be a JSON string
-            assert isinstance(result, str)
-            
-            # The result might be a string representation of a JSON string
-            # Try to parse it directly first, and if that fails, try to parse it as a string representation
-            try:
-                parsed_result = json.loads(result)
-            except json.JSONDecodeError:
-                # If it's a string representation of a JSON string, it will be surrounded by quotes
-                # and have escaped quotes inside
-                if result.startswith('""') and result.endswith('""'):
-                    # Remove the surrounding quotes and unescape the string
-                    unescaped = result[1:-1].replace('\\""', '""')
-                    parsed_result = json.loads(unescaped)
-            
-            assert isinstance(parsed_result, dict)
-            assert parsed_result.get(""name"") == ""John""
-            assert parsed_result.get(""age"") == 30
+            # The result should be a dictionary
+            assert isinstance(result, dict)
+            assert result.get(""name"") == ""John""
+            assert result.get(""age"") == 30
     
     def test_custom_openai_json_conversion_without_error(self, mock_llm_with_function_calling):
         """"""Test that JSON conversion works normally when Instructor doesn't raise an error.""""""
         # Mock Instructor that returns JSON without error
         mock_instructor = Mock()
-        mock_instructor.to_json.return_value = '{""name"": ""John"", ""age"": 30}'
+        mock_instructor.to_json.return_value = {""name"": ""John"", ""age"": 30}
         
         # Create converter with mocked dependencies
         converter = Converter(
@@ -93,7 +79,8 @@ def test_custom_openai_json_conversion_without_error(self, mock_llm_with_functio
             mock_llm_with_function_calling.call.assert_not_called()
             
             # Verify the result matches the expected output
-            assert result == '{""name"": ""John"", ""age"": 30}'
+            assert isinstance(result, dict)
+            assert result == {""name"": ""John"", ""age"": 30}
             
     def test_custom_openai_json_conversion_with_invalid_json(self, mock_llm_with_function_calling):
         """"""Test that JSON conversion handles invalid JSON gracefully.""""""
@@ -117,9 +104,9 @@ def test_custom_openai_json_conversion_with_invalid_json(self, mock_llm_with_fun
         
         # Mock the _create_instructor method to return our mocked instructor
         with patch.object(converter, '_create_instructor', return_value=mock_instructor):
-            # Call to_json method
-            result = converter.to_json()
+            # Call to_json method and expect it to raise a ConverterError
+            with pytest.raises(ConverterError) as excinfo:
+                converter.to_json()
             
-            # The result should be a ConverterError instance
-            assert isinstance(result, ConverterError)
-            assert ""invalid json"" in str(result).lower() or ""expecting value"" in str(result).lower()
+            # Check the error message
+            assert ""invalid json"" in str(excinfo.value).lower() or ""expecting value"" in str(excinfo.value).lower()