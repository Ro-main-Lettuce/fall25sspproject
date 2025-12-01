@@ -1,7 +1,8 @@
 import pytest
-from unittest.mock import MagicMock, patch
+from unittest.mock import MagicMock
 
 from crewai.tools import BaseTool, tool
+from crewai.tools.tool_usage import ToolUsage
 
 
 def test_tool_usage_limit():
@@ -66,3 +67,85 @@ def default_tool(input_text: str) -> str:
     
     assert default_tool.max_usage_count is None
     assert default_tool.current_usage_count == 0
+
+
+def test_invalid_usage_limit():
+    """"""Test that negative usage limits raise ValueError.""""""
+    class ValidTool(BaseTool):
+        name: str = ""Valid Tool""
+        description: str = ""A tool with valid usage limit""
+
+        def _run(self, input_text: str) -> str:
+            return f""Processed {input_text}""
+    
+    with pytest.raises(ValueError, match=""max_usage_count must be a positive integer""):
+        ValidTool(max_usage_count=-1)
+
+
+def test_reset_usage_count():
+    """"""Test that reset_usage_count method works correctly.""""""
+    class LimitedTool(BaseTool):
+        name: str = ""Limited Tool""
+        description: str = ""A tool with usage limits for testing""
+        max_usage_count: int = 3
+
+        def _run(self, input_text: str) -> str:
+            return f""Processed {input_text}""
+
+    tool = LimitedTool()
+    
+    tool.run(input_text=""test1"")
+    tool.run(input_text=""test2"")
+    assert tool.current_usage_count == 2
+    
+    tool.reset_usage_count()
+    assert tool.current_usage_count == 0
+    
+    result = tool.run(input_text=""test3"")
+    assert result == ""Processed test3""
+    assert tool.current_usage_count == 1
+
+
+def test_tool_usage_with_toolusage_class():
+    """"""Test that ToolUsage class correctly enforces usage limits.""""""
+    class LimitedTool(BaseTool):
+        name: str = ""Limited Tool""
+        description: str = ""A tool with usage limits for testing""
+        max_usage_count: int = 2
+
+        def _run(self, input_text: str) -> str:
+            return f""Processed {input_text}""
+
+    tool = LimitedTool()
+    
+    mock_agent = MagicMock()
+    mock_task = MagicMock()
+    mock_tools_handler = MagicMock()
+    
+    tool_usage = ToolUsage(
+        tools=[tool],
+        agent=mock_agent,
+        task=mock_task,
+        tools_handler=mock_tools_handler,
+        function_calling_llm=MagicMock(),
+    )
+    
+    tool_usage._check_tool_repeated_usage = MagicMock(return_value=False)
+    tool_usage._format_result = lambda result: result
+    
+    mock_calling = MagicMock()
+    mock_calling.tool_name = ""Limited Tool""
+    mock_calling.arguments = {""input_text"": ""test""}
+    
+    result1 = tool_usage._check_usage_limit(tool, ""Limited Tool"")
+    assert result1 is None
+    
+    tool.current_usage_count += 1
+    
+    result2 = tool_usage._check_usage_limit(tool, ""Limited Tool"")
+    assert result2 is None
+    
+    tool.current_usage_count += 1
+    
+    result3 = tool_usage._check_usage_limit(tool, ""Limited Tool"")
+    assert ""has reached its usage limit of 2 times"" in result3