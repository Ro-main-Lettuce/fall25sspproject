@@ -3,6 +3,7 @@
 import asyncio
 
 import pytest
+from pydantic import BaseModel
 
 from crewai.flow.flow import Flow, and_, listen, or_, router, start
 
@@ -265,6 +266,81 @@ def step_2(self):
     assert flow.counter == 2
 
 
+def test_flow_uuid_unstructured():
+    """"""Test that unstructured (dictionary) flow states automatically get a UUID that persists.""""""
+    initial_id = None
+
+    class UUIDUnstructuredFlow(Flow):
+        @start()
+        def first_method(self):
+            nonlocal initial_id
+            # Verify ID is automatically generated
+            assert ""id"" in self.state
+            assert isinstance(self.state[""id""], str)
+            # Store initial ID for comparison
+            initial_id = self.state[""id""]
+            # Add some data to trigger state update
+            self.state[""data""] = ""example""
+
+        @listen(first_method)
+        def second_method(self):
+            # Ensure the ID persists after state updates
+            assert ""id"" in self.state
+            assert self.state[""id""] == initial_id
+            # Update state again to verify ID preservation
+            self.state[""more_data""] = ""test""
+            assert self.state[""id""] == initial_id
+
+    flow = UUIDUnstructuredFlow()
+    flow.kickoff()
+    # Verify ID persists after flow completion
+    assert flow.state[""id""] == initial_id
+    # Verify UUID format (36 characters, including hyphens)
+    assert len(flow.state[""id""]) == 36
+
+
+def test_flow_uuid_structured():
+    """"""Test that structured (Pydantic) flow states automatically get a UUID that persists.""""""
+    initial_id = None
+
+    class MyStructuredState(BaseModel):
+        counter: int = 0
+        message: str = ""initial""
+
+    class UUIDStructuredFlow(Flow[MyStructuredState]):
+        @start()
+        def first_method(self):
+            nonlocal initial_id
+            # Verify ID is automatically generated and accessible as attribute
+            assert hasattr(self.state, ""id"")
+            assert isinstance(self.state.id, str)
+            # Store initial ID for comparison
+            initial_id = self.state.id
+            # Update some fields to trigger state changes
+            self.state.counter += 1
+            self.state.message = ""updated""
+
+        @listen(first_method)
+        def second_method(self):
+            # Ensure the ID persists after state updates
+            assert hasattr(self.state, ""id"")
+            assert self.state.id == initial_id
+            # Update state again to verify ID preservation
+            self.state.counter += 1
+            self.state.message = ""final""
+            assert self.state.id == initial_id
+
+    flow = UUIDStructuredFlow()
+    flow.kickoff()
+    # Verify ID persists after flow completion
+    assert flow.state.id == initial_id
+    # Verify UUID format (36 characters, including hyphens)
+    assert len(flow.state.id) == 36
+    # Verify other state fields were properly updated
+    assert flow.state.counter == 2
+    assert flow.state.message == ""final""
+
+
 def test_router_with_multiple_conditions():
     """"""Test a router that triggers when any of multiple steps complete (OR condition),
     and another router that triggers only after all specified steps complete (AND condition).