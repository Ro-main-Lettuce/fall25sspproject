@@ -1,4 +1,4 @@
-from typing import Any, Dict, List, Optional
+from typing import Any
 
 import pytest
 from pydantic import BaseModel
@@ -12,43 +12,43 @@
 # Concrete implementation for testing
 class ConcreteAgentAdapter(BaseAgentAdapter):
     def configure_tools(
-        self, tools: Optional[List[BaseTool]] = None, **kwargs: Any
+        self, tools: list[BaseTool] | None = None, **kwargs: Any,
     ) -> None:
         # Simple implementation for testing
         self.tools = tools or []
 
     def execute_task(
         self,
         task: Any,
-        context: Optional[str] = None,
-        tools: Optional[List[Any]] = None,
+        context: str | None = None,
+        tools: list[Any] | None = None,
     ) -> str:
         # Dummy implementation needed due to BaseAgent inheritance
         return ""Task executed""
 
-    def create_agent_executor(self, tools: Optional[List[BaseTool]] = None) -> Any:
+    def create_agent_executor(self, tools: list[BaseTool] | None = None) -> Any:
         # Dummy implementation
         return None
 
     def get_delegation_tools(
-        self, tools: List[BaseTool], tool_map: Optional[Dict[str, BaseTool]]
-    ) -> List[BaseTool]:
+        self, tools: list[BaseTool], tool_map: dict[str, BaseTool] | None,
+    ) -> list[BaseTool]:
         # Dummy implementation
         return []
 
-    def _parse_output(self, agent_output: Any, token_process: TokenProcess):
+    def _parse_output(self, agent_output: Any, token_process: TokenProcess) -> None:
         # Dummy implementation
         pass
 
-    def get_output_converter(self, tools: Optional[List[BaseTool]] = None) -> Any:
+    def get_output_converter(self, tools: list[BaseTool] | None = None) -> Any:
         # Dummy implementation
         return None
 
 
-def test_base_agent_adapter_initialization():
+def test_base_agent_adapter_initialization() -> None:
     """"""Test initialization of the concrete agent adapter.""""""
     adapter = ConcreteAgentAdapter(
-        role=""test role"", goal=""test goal"", backstory=""test backstory""
+        role=""test role"", goal=""test goal"", backstory=""test backstory"",
     )
     assert isinstance(adapter, BaseAgent)
     assert isinstance(adapter, BaseAgentAdapter)
@@ -57,7 +57,7 @@ def test_base_agent_adapter_initialization():
     assert adapter.adapted_structured_output is False
 
 
-def test_base_agent_adapter_initialization_with_config():
+def test_base_agent_adapter_initialization_with_config() -> None:
     """"""Test initialization with agent_config.""""""
     config = {""model"": ""gpt-4""}
     adapter = ConcreteAgentAdapter(
@@ -69,10 +69,10 @@ def test_base_agent_adapter_initialization_with_config():
     assert adapter._agent_config == config
 
 
-def test_configure_tools_method_exists():
+def test_configure_tools_method_exists() -> None:
     """"""Test that configure_tools method exists and can be called.""""""
     adapter = ConcreteAgentAdapter(
-        role=""test role"", goal=""test goal"", backstory=""test backstory""
+        role=""test role"", goal=""test goal"", backstory=""test backstory"",
     )
     # Create dummy tools if needed, or pass None
     tools = []
@@ -81,10 +81,10 @@ def test_configure_tools_method_exists():
     assert adapter.tools == tools
 
 
-def test_configure_structured_output_method_exists():
+def test_configure_structured_output_method_exists() -> None:
     """"""Test that configure_structured_output method exists and can be called.""""""
     adapter = ConcreteAgentAdapter(
-        role=""test role"", goal=""test goal"", backstory=""test backstory""
+        role=""test role"", goal=""test goal"", backstory=""test backstory"",
     )
 
     # Define a dummy structure or pass None/Any
@@ -95,10 +95,9 @@ class DummyOutput(BaseModel):
     adapter.configure_structured_output(structured_output)
     # Add assertions here if configure_structured_output modifies state
     # For now, just ensuring it runs without error is sufficient
-    pass
 
 
-def test_base_agent_adapter_inherits_base_agent():
+def test_base_agent_adapter_inherits_base_agent() -> None:
     """"""Test that BaseAgentAdapter inherits from BaseAgent.""""""
     assert issubclass(BaseAgentAdapter, BaseAgent)
 
@@ -107,7 +106,7 @@ class ConcreteAgentAdapterWithoutRequiredMethods(BaseAgentAdapter):
     pass
 
 
-def test_base_agent_adapter_fails_without_required_methods():
+def test_base_agent_adapter_fails_without_required_methods() -> None:
     """"""Test that BaseAgentAdapter fails without required methods.""""""
     with pytest.raises(TypeError):
         ConcreteAgentAdapterWithoutRequiredMethods()  # type: ignore