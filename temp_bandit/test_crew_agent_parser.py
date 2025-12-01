@@ -11,19 +11,18 @@
 @pytest.fixture
 def parser():
     agent = MockAgent()
-    p = CrewAgentParser(agent)
-    return p
+    return CrewAgentParser(agent)
 
 
-def test_valid_action_parsing_special_characters(parser):
+def test_valid_action_parsing_special_characters(parser) -> None:
     text = ""Thought: Let's find the temperature
Action: search
Action Input: what's the temperature in SF?""
     result = parser.parse(text)
     assert isinstance(result, AgentAction)
     assert result.tool == ""search""
     assert result.tool_input == ""what's the temperature in SF?""
 
 
-def test_valid_action_parsing_with_json_tool_input(parser):
+def test_valid_action_parsing_with_json_tool_input(parser) -> None:
     text = """"""
     Thought: Let's find the information
     Action: query
@@ -36,173 +35,173 @@ def test_valid_action_parsing_with_json_tool_input(parser):
     assert result.tool_input == expected_tool_input
 
 
-def test_valid_action_parsing_with_quotes(parser):
+def test_valid_action_parsing_with_quotes(parser) -> None:
     text = 'Thought: Let\'s find the temperature
Action: search
Action Input: ""temperature in SF""'
     result = parser.parse(text)
     assert isinstance(result, AgentAction)
     assert result.tool == ""search""
     assert result.tool_input == ""temperature in SF""
 
 
-def test_valid_action_parsing_with_curly_braces(parser):
+def test_valid_action_parsing_with_curly_braces(parser) -> None:
     text = ""Thought: Let's find the temperature
Action: search
Action Input: {temperature in SF}""
     result = parser.parse(text)
     assert isinstance(result, AgentAction)
     assert result.tool == ""search""
     assert result.tool_input == ""{temperature in SF}""
 
 
-def test_valid_action_parsing_with_angle_brackets(parser):
+def test_valid_action_parsing_with_angle_brackets(parser) -> None:
     text = ""Thought: Let's find the temperature
Action: search
Action Input: <temperature in SF>""
     result = parser.parse(text)
     assert isinstance(result, AgentAction)
     assert result.tool == ""search""
     assert result.tool_input == ""<temperature in SF>""
 
 
-def test_valid_action_parsing_with_parentheses(parser):
+def test_valid_action_parsing_with_parentheses(parser) -> None:
     text = ""Thought: Let's find the temperature
Action: search
Action Input: (temperature in SF)""
     result = parser.parse(text)
     assert isinstance(result, AgentAction)
     assert result.tool == ""search""
     assert result.tool_input == ""(temperature in SF)""
 
 
-def test_valid_action_parsing_with_mixed_brackets(parser):
+def test_valid_action_parsing_with_mixed_brackets(parser) -> None:
     text = ""Thought: Let's find the temperature
Action: search
Action Input: [temperature in {SF}]""
     result = parser.parse(text)
     assert isinstance(result, AgentAction)
     assert result.tool == ""search""
     assert result.tool_input == ""[temperature in {SF}]""
 
 
-def test_valid_action_parsing_with_nested_quotes(parser):
+def test_valid_action_parsing_with_nested_quotes(parser) -> None:
     text = ""Thought: Let's find the temperature
Action: search
Action Input: \""what's the temperature in 'SF'?\""""
     result = parser.parse(text)
     assert isinstance(result, AgentAction)
     assert result.tool == ""search""
     assert result.tool_input == ""what's the temperature in 'SF'?""
 
 
-def test_valid_action_parsing_with_incomplete_json(parser):
+def test_valid_action_parsing_with_incomplete_json(parser) -> None:
     text = 'Thought: Let\'s find the temperature
Action: search
Action Input: {""query"": ""temperature in SF""'
     result = parser.parse(text)
     assert isinstance(result, AgentAction)
     assert result.tool == ""search""
     assert result.tool_input == '{""query"": ""temperature in SF""}'
 
 
-def test_valid_action_parsing_with_special_characters(parser):
+def test_valid_action_parsing_with_special_characters(parser) -> None:
     text = ""Thought: Let's find the temperature
Action: search
Action Input: what is the temperature in SF? @$%^&*""
     result = parser.parse(text)
     assert isinstance(result, AgentAction)
     assert result.tool == ""search""
     assert result.tool_input == ""what is the temperature in SF? @$%^&*""
 
 
-def test_valid_action_parsing_with_combination(parser):
+def test_valid_action_parsing_with_combination(parser) -> None:
     text = 'Thought: Let\'s find the temperature
Action: search
Action Input: ""[what is the temperature in SF?]""'
     result = parser.parse(text)
     assert isinstance(result, AgentAction)
     assert result.tool == ""search""
     assert result.tool_input == ""[what is the temperature in SF?]""
 
 
-def test_valid_action_parsing_with_mixed_quotes(parser):
+def test_valid_action_parsing_with_mixed_quotes(parser) -> None:
     text = ""Thought: Let's find the temperature
Action: search
Action Input: \""what's the temperature in SF?\""""
     result = parser.parse(text)
     assert isinstance(result, AgentAction)
     assert result.tool == ""search""
     assert result.tool_input == ""what's the temperature in SF?""
 
 
-def test_valid_action_parsing_with_newlines(parser):
+def test_valid_action_parsing_with_newlines(parser) -> None:
     text = ""Thought: Let's find the temperature
Action: search
Action Input: what is
the temperature in SF?""
     result = parser.parse(text)
     assert isinstance(result, AgentAction)
     assert result.tool == ""search""
     assert result.tool_input == ""what is
the temperature in SF?""
 
 
-def test_valid_action_parsing_with_escaped_characters(parser):
+def test_valid_action_parsing_with_escaped_characters(parser) -> None:
     text = ""Thought: Let's find the temperature
Action: search
Action Input: what is the temperature in SF? \
""
     result = parser.parse(text)
     assert isinstance(result, AgentAction)
     assert result.tool == ""search""
     assert result.tool_input == ""what is the temperature in SF? \
""
 
 
-def test_valid_action_parsing_with_json_string(parser):
+def test_valid_action_parsing_with_json_string(parser) -> None:
     text = 'Thought: Let\'s find the temperature
Action: search
Action Input: {""query"": ""temperature in SF""}'
     result = parser.parse(text)
     assert isinstance(result, AgentAction)
     assert result.tool == ""search""
     assert result.tool_input == '{""query"": ""temperature in SF""}'
 
 
-def test_valid_action_parsing_with_unbalanced_quotes(parser):
+def test_valid_action_parsing_with_unbalanced_quotes(parser) -> None:
     text = ""Thought: Let's find the temperature
Action: search
Action Input: \""what is the temperature in SF?""
     result = parser.parse(text)
     assert isinstance(result, AgentAction)
     assert result.tool == ""search""
     assert result.tool_input == ""what is the temperature in SF?""
 
 
-def test_clean_action_no_formatting(parser):
+def test_clean_action_no_formatting(parser) -> None:
     action = ""Ask question to senior researcher""
     cleaned_action = parser._clean_action(action)
     assert cleaned_action == ""Ask question to senior researcher""
 
 
-def test_clean_action_with_leading_asterisks(parser):
+def test_clean_action_with_leading_asterisks(parser) -> None:
     action = ""** Ask question to senior researcher""
     cleaned_action = parser._clean_action(action)
     assert cleaned_action == ""Ask question to senior researcher""
 
 
-def test_clean_action_with_trailing_asterisks(parser):
+def test_clean_action_with_trailing_asterisks(parser) -> None:
     action = ""Ask question to senior researcher **""
     cleaned_action = parser._clean_action(action)
     assert cleaned_action == ""Ask question to senior researcher""
 
 
-def test_clean_action_with_leading_and_trailing_asterisks(parser):
+def test_clean_action_with_leading_and_trailing_asterisks(parser) -> None:
     action = ""** Ask question to senior researcher **""
     cleaned_action = parser._clean_action(action)
     assert cleaned_action == ""Ask question to senior researcher""
 
 
-def test_clean_action_with_multiple_leading_asterisks(parser):
+def test_clean_action_with_multiple_leading_asterisks(parser) -> None:
     action = ""**** Ask question to senior researcher""
     cleaned_action = parser._clean_action(action)
     assert cleaned_action == ""Ask question to senior researcher""
 
 
-def test_clean_action_with_multiple_trailing_asterisks(parser):
+def test_clean_action_with_multiple_trailing_asterisks(parser) -> None:
     action = ""Ask question to senior researcher ****""
     cleaned_action = parser._clean_action(action)
     assert cleaned_action == ""Ask question to senior researcher""
 
 
-def test_clean_action_with_spaces_and_asterisks(parser):
+def test_clean_action_with_spaces_and_asterisks(parser) -> None:
     action = ""  **  Ask question to senior researcher  **  ""
     cleaned_action = parser._clean_action(action)
     assert cleaned_action == ""Ask question to senior researcher""
 
 
-def test_clean_action_with_only_asterisks(parser):
+def test_clean_action_with_only_asterisks(parser) -> None:
     action = ""****""
     cleaned_action = parser._clean_action(action)
     assert cleaned_action == """"
 
 
-def test_clean_action_with_empty_string(parser):
+def test_clean_action_with_empty_string(parser) -> None:
     action = """"
     cleaned_action = parser._clean_action(action)
     assert cleaned_action == """"
 
 
-def test_valid_final_answer_parsing(parser):
+def test_valid_final_answer_parsing(parser) -> None:
     text = (
         ""Thought: I found the information
Final Answer: The temperature is 100 degrees""
     )
@@ -211,36 +210,36 @@ def test_valid_final_answer_parsing(parser):
     assert result.output == ""The temperature is 100 degrees""
 
 
-def test_missing_action_error(parser):
+def test_missing_action_error(parser) -> None:
     text = ""Thought: Let's find the temperature
Action Input: what is the temperature in SF?""
     with pytest.raises(OutputParserException) as exc_info:
         parser.parse(text)
     assert ""Invalid Format: I missed the 'Action:' after 'Thought:'."" in str(
-        exc_info.value
+        exc_info.value,
     )
 
 
-def test_missing_action_input_error(parser):
+def test_missing_action_input_error(parser) -> None:
     text = ""Thought: Let's find the temperature
Action: search""
     with pytest.raises(OutputParserException) as exc_info:
         parser.parse(text)
     assert ""I missed the 'Action Input:' after 'Action:'."" in str(exc_info.value)
 
 
-def test_safe_repair_json(parser):
+def test_safe_repair_json(parser) -> None:
     invalid_json = '{""task"": ""Research XAI"", ""context"": ""Explainable AI"", ""coworker"": Senior Researcher'
     expected_repaired_json = '{""task"": ""Research XAI"", ""context"": ""Explainable AI"", ""coworker"": ""Senior Researcher""}'
     result = parser._safe_repair_json(invalid_json)
     assert result == expected_repaired_json
 
 
-def test_safe_repair_json_unrepairable(parser):
+def test_safe_repair_json_unrepairable(parser) -> None:
     invalid_json = ""{invalid_json""
     result = parser._safe_repair_json(invalid_json)
     assert result == invalid_json  # Should return the original if unrepairable
 
 
-def test_safe_repair_json_missing_quotes(parser):
+def test_safe_repair_json_missing_quotes(parser) -> None:
     invalid_json = (
         '{task: ""Research XAI"", context: ""Explainable AI"", coworker: Senior Researcher}'
     )
@@ -249,93 +248,93 @@ def test_safe_repair_json_missing_quotes(parser):
     assert result == expected_repaired_json
 
 
-def test_safe_repair_json_unclosed_brackets(parser):
+def test_safe_repair_json_unclosed_brackets(parser) -> None:
     invalid_json = '{""task"": ""Research XAI"", ""context"": ""Explainable AI"", ""coworker"": ""Senior Researcher""'
     expected_repaired_json = '{""task"": ""Research XAI"", ""context"": ""Explainable AI"", ""coworker"": ""Senior Researcher""}'
     result = parser._safe_repair_json(invalid_json)
     assert result == expected_repaired_json
 
 
-def test_safe_repair_json_extra_commas(parser):
+def test_safe_repair_json_extra_commas(parser) -> None:
     invalid_json = '{""task"": ""Research XAI"", ""context"": ""Explainable AI"", ""coworker"": ""Senior Researcher"",}'
     expected_repaired_json = '{""task"": ""Research XAI"", ""context"": ""Explainable AI"", ""coworker"": ""Senior Researcher""}'
     result = parser._safe_repair_json(invalid_json)
     assert result == expected_repaired_json
 
 
-def test_safe_repair_json_trailing_commas(parser):
+def test_safe_repair_json_trailing_commas(parser) -> None:
     invalid_json = '{""task"": ""Research XAI"", ""context"": ""Explainable AI"", ""coworker"": ""Senior Researcher"",}'
     expected_repaired_json = '{""task"": ""Research XAI"", ""context"": ""Explainable AI"", ""coworker"": ""Senior Researcher""}'
     result = parser._safe_repair_json(invalid_json)
     assert result == expected_repaired_json
 
 
-def test_safe_repair_json_single_quotes(parser):
+def test_safe_repair_json_single_quotes(parser) -> None:
     invalid_json = ""{'task': 'Research XAI', 'context': 'Explainable AI', 'coworker': 'Senior Researcher'}""
     expected_repaired_json = '{""task"": ""Research XAI"", ""context"": ""Explainable AI"", ""coworker"": ""Senior Researcher""}'
     result = parser._safe_repair_json(invalid_json)
     assert result == expected_repaired_json
 
 
-def test_safe_repair_json_mixed_quotes(parser):
+def test_safe_repair_json_mixed_quotes(parser) -> None:
     invalid_json = ""{'task': \""Research XAI\"", 'context': \""Explainable AI\"", 'coworker': 'Senior Researcher'}""
     expected_repaired_json = '{""task"": ""Research XAI"", ""context"": ""Explainable AI"", ""coworker"": ""Senior Researcher""}'
     result = parser._safe_repair_json(invalid_json)
     assert result == expected_repaired_json
 
 
-def test_safe_repair_json_unescaped_characters(parser):
+def test_safe_repair_json_unescaped_characters(parser) -> None:
     invalid_json = '{""task"": ""Research XAI"", ""context"": ""Explainable AI"", ""coworker"": ""Senior Researcher
""}'
     expected_repaired_json = '{""task"": ""Research XAI"", ""context"": ""Explainable AI"", ""coworker"": ""Senior Researcher""}'
     result = parser._safe_repair_json(invalid_json)
     assert result == expected_repaired_json
 
 
-def test_safe_repair_json_missing_colon(parser):
+def test_safe_repair_json_missing_colon(parser) -> None:
     invalid_json = '{""task"" ""Research XAI"", ""context"": ""Explainable AI"", ""coworker"": ""Senior Researcher""}'
     expected_repaired_json = '{""task"": ""Research XAI"", ""context"": ""Explainable AI"", ""coworker"": ""Senior Researcher""}'
     result = parser._safe_repair_json(invalid_json)
     assert result == expected_repaired_json
 
 
-def test_safe_repair_json_missing_comma(parser):
+def test_safe_repair_json_missing_comma(parser) -> None:
     invalid_json = '{""task"": ""Research XAI"" ""context"": ""Explainable AI"", ""coworker"": ""Senior Researcher""}'
     expected_repaired_json = '{""task"": ""Research XAI"", ""context"": ""Explainable AI"", ""coworker"": ""Senior Researcher""}'
     result = parser._safe_repair_json(invalid_json)
     assert result == expected_repaired_json
 
 
-def test_safe_repair_json_unexpected_trailing_characters(parser):
+def test_safe_repair_json_unexpected_trailing_characters(parser) -> None:
     invalid_json = '{""task"": ""Research XAI"", ""context"": ""Explainable AI"", ""coworker"": ""Senior Researcher""} random text'
     expected_repaired_json = '{""task"": ""Research XAI"", ""context"": ""Explainable AI"", ""coworker"": ""Senior Researcher""}'
     result = parser._safe_repair_json(invalid_json)
     assert result == expected_repaired_json
 
 
-def test_safe_repair_json_special_characters_key(parser):
+def test_safe_repair_json_special_characters_key(parser) -> None:
     invalid_json = '{""task!@#"": ""Research XAI"", ""context$%^"": ""Explainable AI"", ""coworker&*()"": ""Senior Researcher""}'
     expected_repaired_json = '{""task!@#"": ""Research XAI"", ""context$%^"": ""Explainable AI"", ""coworker&*()"": ""Senior Researcher""}'
     result = parser._safe_repair_json(invalid_json)
     assert result == expected_repaired_json
 
 
-def test_parsing_with_whitespace(parser):
+def test_parsing_with_whitespace(parser) -> None:
     text = "" Thought: Let's find the temperature 
 Action: search 
 Action Input: what is the temperature in SF? ""
     result = parser.parse(text)
     assert isinstance(result, AgentAction)
     assert result.tool == ""search""
     assert result.tool_input == ""what is the temperature in SF?""
 
 
-def test_parsing_with_special_characters(parser):
+def test_parsing_with_special_characters(parser) -> None:
     text = 'Thought: Let\'s find the temperature
Action: search
Action Input: ""what is the temperature in SF?""'
     result = parser.parse(text)
     assert isinstance(result, AgentAction)
     assert result.tool == ""search""
     assert result.tool_input == ""what is the temperature in SF?""
 
 
-def test_integration_valid_and_invalid(parser):
+def test_integration_valid_and_invalid(parser) -> None:
     text = """"""
     Thought: Let's find the temperature
     Action: search
@@ -366,7 +365,7 @@ def test_integration_valid_and_invalid(parser):
 
 
 class MockAgent:
-    def increment_formatting_errors(self):
+    def increment_formatting_errors(self) -> None:
         pass
 
 