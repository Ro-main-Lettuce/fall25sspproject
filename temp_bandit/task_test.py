@@ -719,61 +719,62 @@ def test_interpolate_inputs():
     task = Task(
         description=""Give me a list of 5 interesting ideas about {topic} to explore for an article, what makes them unique and interesting."",
         expected_output=""Bullet point list of 5 interesting ideas about {topic}."",
+        output_file=""/tmp/{topic}/output_{date}.txt"",
     )
 
-    task.interpolate_inputs(inputs={""topic"": ""AI""})
+    task.interpolate_inputs_and_add_conversation_history(
+        inputs={""topic"": ""AI"", ""date"": ""2024""}
+    )
     assert (
         task.description
         == ""Give me a list of 5 interesting ideas about AI to explore for an article, what makes them unique and interesting.""
     )
     assert task.expected_output == ""Bullet point list of 5 interesting ideas about AI.""
+    assert task.output_file == ""/tmp/AI/output_2024.txt""
 
-    task.interpolate_inputs(inputs={""topic"": ""ML""})
+    task.interpolate_inputs_and_add_conversation_history(
+        inputs={""topic"": ""ML"", ""date"": ""2025""}
+    )
     assert (
         task.description
         == ""Give me a list of 5 interesting ideas about ML to explore for an article, what makes them unique and interesting.""
     )
     assert task.expected_output == ""Bullet point list of 5 interesting ideas about ML.""
+    assert task.output_file == ""/tmp/ML/output_2025.txt""
 
 
 def test_interpolate_only():
     """"""Test the interpolate_only method for various scenarios including JSON structure preservation.""""""
     task = Task(
-        description=""Unused in this test"",
-        expected_output=""Unused in this test""
+        description=""Unused in this test"", expected_output=""Unused in this test""
     )
-    
+
     # Test JSON structure preservation
     json_string = '{""info"": ""Look at {placeholder}"", ""nested"": {""val"": ""{nestedVal}""}}'
     result = task.interpolate_only(
         input_string=json_string,
-        inputs={""placeholder"": ""the data"", ""nestedVal"": ""something else""}
+        inputs={""placeholder"": ""the data"", ""nestedVal"": ""something else""},
     )
     assert '""info"": ""Look at the data""' in result
     assert '""val"": ""something else""' in result
     assert ""{placeholder}"" not in result
     assert ""{nestedVal}"" not in result
-    
+
     # Test normal string interpolation
     normal_string = ""Hello {name}, welcome to {place}!""
     result = task.interpolate_only(
-        input_string=normal_string,
-        inputs={""name"": ""John"", ""place"": ""CrewAI""}
+        input_string=normal_string, inputs={""name"": ""John"", ""place"": ""CrewAI""}
     )
     assert result == ""Hello John, welcome to CrewAI!""
-    
+
     # Test empty string
-    result = task.interpolate_only(
-        input_string="""",
-        inputs={""unused"": ""value""}
-    )
+    result = task.interpolate_only(input_string="""", inputs={""unused"": ""value""})
     assert result == """"
-    
+
     # Test string with no placeholders
     no_placeholders = ""Hello, this is a test""
     result = task.interpolate_only(
-        input_string=no_placeholders,
-        inputs={""unused"": ""value""}
+        input_string=no_placeholders, inputs={""unused"": ""value""}
     )
     assert result == no_placeholders
 
@@ -868,7 +869,100 @@ def test_key():
 
     assert task.key == hash, ""The key should be the hash of the description.""
 
-    task.interpolate_inputs(inputs={""topic"": ""AI""})
+    task.interpolate_inputs_and_add_conversation_history(inputs={""topic"": ""AI""})
     assert (
         task.key == hash
     ), ""The key should be the hash of the non-interpolated description.""
+
+
+def test_output_file_validation():
+    """"""Test output file path validation.""""""
+    # Valid paths
+    assert (
+        Task(
+            description=""Test task"",
+            expected_output=""Test output"",
+            output_file=""output.txt"",
+        ).output_file
+        == ""output.txt""
+    )
+    assert (
+        Task(
+            description=""Test task"",
+            expected_output=""Test output"",
+            output_file=""/tmp/output.txt"",
+        ).output_file
+        == ""tmp/output.txt""
+    )
+    assert (
+        Task(
+            description=""Test task"",
+            expected_output=""Test output"",
+            output_file=""{dir}/output_{date}.txt"",
+        ).output_file
+        == ""{dir}/output_{date}.txt""
+    )
+
+    # Invalid paths
+    with pytest.raises(ValueError, match=""Path traversal""):
+        Task(
+            description=""Test task"",
+            expected_output=""Test output"",
+            output_file=""../output.txt"",
+        )
+    with pytest.raises(ValueError, match=""Path traversal""):
+        Task(
+            description=""Test task"",
+            expected_output=""Test output"",
+            output_file=""folder/../output.txt"",
+        )
+    with pytest.raises(ValueError, match=""Shell special characters""):
+        Task(
+            description=""Test task"",
+            expected_output=""Test output"",
+            output_file=""output.txt | rm -rf /"",
+        )
+    with pytest.raises(ValueError, match=""Shell expansion""):
+        Task(
+            description=""Test task"",
+            expected_output=""Test output"",
+            output_file=""~/output.txt"",
+        )
+    with pytest.raises(ValueError, match=""Shell expansion""):
+        Task(
+            description=""Test task"",
+            expected_output=""Test output"",
+            output_file=""$HOME/output.txt"",
+        )
+    with pytest.raises(ValueError, match=""Invalid template variable""):
+        Task(
+            description=""Test task"",
+            expected_output=""Test output"",
+            output_file=""{invalid-name}/output.txt"",
+        )
+
+
+@pytest.mark.vcr(filter_headers=[""authorization""])
+def test_task_execution_times():
+    researcher = Agent(
+        role=""Researcher"",
+        goal=""Make the best research and analysis on content about AI and AI agents"",
+        backstory=""You're an expert researcher, specialized in technology, software engineering, AI and startups. You work as a freelancer and is now working on doing research and analysis for a new customer."",
+        allow_delegation=False,
+    )
+
+    task = Task(
+        description=""Give me a list of 5 interesting ideas to explore for na article, what makes them unique and interesting."",
+        expected_output=""Bullet point list of 5 interesting ideas."",
+        agent=researcher,
+    )
+
+    assert task.start_time is None
+    assert task.end_time is None
+    assert task.execution_duration is None
+
+    task.execute_sync(agent=researcher)
+
+    assert task.start_time is not None
+    assert task.end_time is not None
+    assert task.execution_duration == (task.end_time - task.start_time).total_seconds()