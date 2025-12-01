@@ -1,4 +1,5 @@
 import pytest
+import logging
 from crewai.utilities.events.llm_events import LLMCallStartedEvent
 from crewai.utilities.token_counter_callback import TokenCalcHandler
 from crewai.agents.agent_builder.utilities.base_token_process import TokenProcess
@@ -133,3 +134,70 @@ def test_available_functions_preserved(self):
         
         assert event.tools == [{""name"": ""tool1""}]
         assert event.available_functions == available_funcs
+
+    @pytest.mark.parametrize(""tools_input,expected"", [
+        ([{""name"": ""tool1""}, TokenCalcHandler(TokenProcess())], [{""name"": ""tool1""}]),
+        ([{""name"": ""tool1""}, ""string_tool"", {""name"": ""tool2""}], [{""name"": ""tool1""}, {""name"": ""tool2""}]),
+        ([TokenCalcHandler(TokenProcess()), 123, [""list_tool""]], []),
+        ([{""name"": ""tool1"", ""type"": ""function"", ""enabled"": True}], [{""name"": ""tool1"", ""type"": ""function"", ""enabled"": True}]),
+        ([], []),
+        (None, None),
+    ])
+    def test_tools_sanitization_parameterized(self, tools_input, expected):
+        """"""Parameterized test for various tools sanitization scenarios""""""
+        event = LLMCallStartedEvent(
+            messages=[{""role"": ""user"", ""content"": ""test message""}],
+            tools=tools_input,
+            callbacks=None
+        )
+        assert event.tools == expected
+
+    def test_tools_with_invalid_dict_values_filtered(self):
+        """"""Test that dicts with invalid value types are filtered out""""""
+        class CustomObject:
+            pass
+        
+        invalid_tool = {""name"": ""tool1"", ""custom_obj"": CustomObject()}
+        valid_tool = {""name"": ""tool2"", ""type"": ""function""}
+        
+        event = LLMCallStartedEvent(
+            messages=[{""role"": ""user"", ""content"": ""test message""}],
+            tools=[valid_tool, invalid_tool],
+            callbacks=None
+        )
+        
+        assert event.tools == [valid_tool]
+
+    def test_sanitize_tools_performance_large_dataset(self):
+        """"""Test sanitization performance with large datasets""""""
+        token_handler = TokenCalcHandler(TokenProcess())
+        
+        large_tools_list = []
+        for i in range(1000):
+            if i % 3 == 0:
+                large_tools_list.append({""name"": f""tool_{i}"", ""type"": ""function""})
+            elif i % 3 == 1:
+                large_tools_list.append(token_handler)
+            else:
+                large_tools_list.append(f""string_tool_{i}"")
+        
+        event = LLMCallStartedEvent(
+            messages=[{""role"": ""user"", ""content"": ""test message""}],
+            tools=large_tools_list,
+            callbacks=None
+        )
+        
+        expected_count = len([i for i in range(1000) if i % 3 == 0])
+        assert len(event.tools) == expected_count
+        assert all(isinstance(tool, dict) for tool in event.tools)
+
+    def test_sanitization_error_handling(self, caplog):
+        """"""Test that sanitization errors are handled gracefully""""""
+        with caplog.at_level(logging.WARNING):
+            event = LLMCallStartedEvent(
+                messages=[{""role"": ""user"", ""content"": ""test message""}],
+                tools=[{""name"": ""tool1""}, TokenCalcHandler(TokenProcess())],
+                callbacks=None
+            )
+            
+            assert event.tools == [{""name"": ""tool1""}]