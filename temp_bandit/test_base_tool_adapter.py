@@ -1,4 +1,3 @@
-from typing import Any, List
 from unittest.mock import Mock
 
 import pytest
@@ -8,7 +7,7 @@
 
 
 class ConcreteToolAdapter(BaseToolAdapter):
-    def configure_tools(self, tools: List[BaseTool]) -> None:
+    def configure_tools(self, tools: list[BaseTool]) -> None:
         self.converted_tools = [f""converted_{tool.name}"" for tool in tools]
 
 
@@ -31,19 +30,19 @@ def tools_list(mock_tool_1, mock_tool_2):
     return [mock_tool_1, mock_tool_2]
 
 
-def test_initialization_with_tools(tools_list):
+def test_initialization_with_tools(tools_list) -> None:
     adapter = ConcreteToolAdapter(tools=tools_list)
     assert adapter.original_tools == tools_list
     assert adapter.converted_tools == []  # Conversion happens in configure_tools
 
 
-def test_initialization_without_tools():
+def test_initialization_without_tools() -> None:
     adapter = ConcreteToolAdapter()
     assert adapter.original_tools == []
     assert adapter.converted_tools == []
 
 
-def test_configure_tools(tools_list):
+def test_configure_tools(tools_list) -> None:
     adapter = ConcreteToolAdapter()
     adapter.configure_tools(tools_list)
     assert adapter.converted_tools == [""converted_Mock Tool 1"", ""converted_MockTool2""]
@@ -58,28 +57,28 @@ def test_configure_tools(tools_list):
     assert adapter_with_init_tools.original_tools == tools_list
 
 
-def test_tools_method(tools_list):
+def test_tools_method(tools_list) -> None:
     adapter = ConcreteToolAdapter()
     adapter.configure_tools(tools_list)
     assert adapter.tools() == [""converted_Mock Tool 1"", ""converted_MockTool2""]
 
 
-def test_tools_method_empty():
+def test_tools_method_empty() -> None:
     adapter = ConcreteToolAdapter()
     assert adapter.tools() == []
 
 
-def test_sanitize_tool_name_with_spaces():
+def test_sanitize_tool_name_with_spaces() -> None:
     adapter = ConcreteToolAdapter()
     assert adapter.sanitize_tool_name(""Tool With Spaces"") == ""Tool_With_Spaces""
 
 
-def test_sanitize_tool_name_without_spaces():
+def test_sanitize_tool_name_without_spaces() -> None:
     adapter = ConcreteToolAdapter()
     assert adapter.sanitize_tool_name(""ToolWithoutSpaces"") == ""ToolWithoutSpaces""
 
 
-def test_sanitize_tool_name_empty():
+def test_sanitize_tool_name_empty() -> None:
     adapter = ConcreteToolAdapter()
     assert adapter.sanitize_tool_name("""") == """"
 
@@ -88,7 +87,7 @@ class ConcreteToolAdapterWithoutRequiredMethods(BaseToolAdapter):
     pass
 
 
-def test_tool_adapted_fails_without_required_methods():
+def test_tool_adapted_fails_without_required_methods() -> None:
     """"""Test that BaseToolAdapter fails without required methods.""""""
     with pytest.raises(TypeError):
         ConcreteToolAdapterWithoutRequiredMethods()  # type: ignore