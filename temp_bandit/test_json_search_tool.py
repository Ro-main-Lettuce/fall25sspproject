@@ -26,3 +26,36 @@ def test_json_search_tool_with_invalid_query():
     
     with pytest.raises(ValueError, match=""search_query must be a string or a dictionary with a 'description' key""):
         tool.run(123)  # Not a string or dict with description
+
+
+def test_json_search_tool_with_empty_string():
+    """"""Test JSONSearchTool with an empty string.""""""
+    tool = JSONSearchTool(json_path=""example.json"")
+    tool._run = lambda search_query, **kwargs: f""Query: {search_query}""
+    
+    result = tool.run("""")
+    assert ""Query: "" == result
+
+
+def test_json_search_tool_with_invalid_dict_format():
+    """"""Test JSONSearchTool with invalid dictionary format.""""""
+    tool = JSONSearchTool(json_path=""example.json"")
+    
+    with pytest.raises(ValueError, match=""Dictionary input must contain a 'description' key""):
+        tool.run({""wrong_key"": ""test query""})
+
+
+def test_json_search_tool_with_none_value():
+    """"""Test JSONSearchTool with None value.""""""
+    tool = JSONSearchTool(json_path=""example.json"")
+    
+    with pytest.raises(ValueError, match=""search_query must be a string or a dictionary with a 'description' key""):
+        tool.run(None)
+
+
+def test_json_search_tool_with_non_string_description():
+    """"""Test JSONSearchTool with non-string description value.""""""
+    tool = JSONSearchTool(json_path=""example.json"")
+    
+    with pytest.raises(ValueError, match=""Description value must be a string""):
+        tool.run({""description"": 123})