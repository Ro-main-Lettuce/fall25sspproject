@@ -1383,6 +1383,25 @@ def _run(self, arg: str) -> str:
     })
     assert ""Tool Arguments: {'arg': {'description': 'test arg', 'type': 'str'}}"" in agent.backstory
 
+def test_interpolate_only_error_handling():
+    agent = Agent(
+        role=""{topic} specialist"",
+        goal=""Figure {goal} out"",
+        backstory=""I am the master of {role}"",
+    )
+    
+    # Test empty input string
+    with pytest.raises(ValueError, match=""Input string cannot be None or empty""):
+        agent._interpolate_only("""", {""topic"": ""AI""})
+        
+    # Test empty inputs dictionary
+    with pytest.raises(ValueError, match=""Inputs dictionary cannot be empty""):
+        agent._interpolate_only(""test {topic}"", {})
+        
+    # Test missing template variable
+    with pytest.raises(KeyError, match=""Missing required template variable""):
+        agent._interpolate_only(""test {missing}"", {""topic"": ""AI""})
+
 def test_agent_with_all_llm_attributes():
     agent = Agent(
         role=""test role"",