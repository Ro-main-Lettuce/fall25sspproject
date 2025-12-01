@@ -121,3 +121,113 @@ def test_tool_usage_render():
         ""Tool Name: Random Number Generator
Tool Arguments: {'min_value': {'description': 'The minimum value of the range (inclusive)', 'type': 'int'}, 'max_value': {'description': 'The maximum value of the range (inclusive)', 'type': 'int'}}
Tool Description: Generates a random number within a specified range""
         in rendered
     )
+
+
+def test_validate_tool_input_booleans_and_none():
+    # Create a ToolUsage instance with mocks
+    tool_usage = ToolUsage(
+        tools_handler=MagicMock(),
+        tools=[],
+        original_tools=[],
+        tools_description="""",
+        tools_names="""",
+        task=MagicMock(),
+        function_calling_llm=MagicMock(),
+        agent=MagicMock(),
+        action=MagicMock(),
+    )
+
+    # Input with booleans and None
+    tool_input = '{""key1"": True, ""key2"": False, ""key3"": None}'
+    expected_arguments = {""key1"": True, ""key2"": False, ""key3"": None}
+
+    arguments = tool_usage._validate_tool_input(tool_input)
+    assert arguments == expected_arguments
+
+
+def test_validate_tool_input_mixed_types():
+    # Create a ToolUsage instance with mocks
+    tool_usage = ToolUsage(
+        tools_handler=MagicMock(),
+        tools=[],
+        original_tools=[],
+        tools_description="""",
+        tools_names="""",
+        task=MagicMock(),
+        function_calling_llm=MagicMock(),
+        agent=MagicMock(),
+        action=MagicMock(),
+    )
+
+    # Input with mixed types
+    tool_input = '{""number"": 123, ""text"": ""Some text"", ""flag"": True}'
+    expected_arguments = {""number"": 123, ""text"": ""Some text"", ""flag"": True}
+
+    arguments = tool_usage._validate_tool_input(tool_input)
+    assert arguments == expected_arguments
+
+
+def test_validate_tool_input_single_quotes():
+    # Create a ToolUsage instance with mocks
+    tool_usage = ToolUsage(
+        tools_handler=MagicMock(),
+        tools=[],
+        original_tools=[],
+        tools_description="""",
+        tools_names="""",
+        task=MagicMock(),
+        function_calling_llm=MagicMock(),
+        agent=MagicMock(),
+        action=MagicMock(),
+    )
+
+    # Input with single quotes instead of double quotes
+    tool_input = ""{'key': 'value', 'flag': True}""
+    expected_arguments = {""key"": ""value"", ""flag"": True}
+
+    arguments = tool_usage._validate_tool_input(tool_input)
+    assert arguments == expected_arguments
+
+
+def test_validate_tool_input_invalid_json_repairable():
+    # Create a ToolUsage instance with mocks
+    tool_usage = ToolUsage(
+        tools_handler=MagicMock(),
+        tools=[],
+        original_tools=[],
+        tools_description="""",
+        tools_names="""",
+        task=MagicMock(),
+        function_calling_llm=MagicMock(),
+        agent=MagicMock(),
+        action=MagicMock(),
+    )
+
+    # Invalid JSON input that can be repaired
+    tool_input = '{""key"": ""value"", ""list"": [1, 2, 3,]}'
+    expected_arguments = {""key"": ""value"", ""list"": [1, 2, 3]}
+
+    arguments = tool_usage._validate_tool_input(tool_input)
+    assert arguments == expected_arguments
+
+
+def test_validate_tool_input_with_special_characters():
+    # Create a ToolUsage instance with mocks
+    tool_usage = ToolUsage(
+        tools_handler=MagicMock(),
+        tools=[],
+        original_tools=[],
+        tools_description="""",
+        tools_names="""",
+        task=MagicMock(),
+        function_calling_llm=MagicMock(),
+        agent=MagicMock(),
+        action=MagicMock(),
+    )
+
+    # Input with special characters
+    tool_input = '{""message"": ""Hello, world! \u263A"", ""valid"": True}'
+    expected_arguments = {""message"": ""Hello, world! ☺"", ""valid"": True}
+
+    arguments = tool_usage._validate_tool_input(tool_input)
+    assert arguments == expected_arguments