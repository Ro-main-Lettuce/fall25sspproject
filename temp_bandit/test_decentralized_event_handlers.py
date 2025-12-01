@@ -12,6 +12,7 @@ def DecentralizedEventHandlers():
 
     class TestState(rx.State):
         count: int = 0
+        value: int = 0
 
         @rx.event
         def increment(self):
@@ -36,11 +37,23 @@ def reset_count(state: TestState):
         """"""
         state.count = 0
 
+    @rx.event
+    def set_value(state: TestState, value: str):
+        """"""Set the value with a parameter.
+
+        Args:
+            state: The state to modify.
+            value: The value to set.
+        """"""
+        state.value = int(value)
+
     def index():
         return rx.vstack(
             rx.heading(TestState.count, id=""counter""),
+            rx.heading(TestState.value, id=""value""),
             rx.button(""Increment"", on_click=TestState.increment, id=""increment""),
             rx.button(""Reset"", on_click=reset_count, id=""reset""),
+            rx.button(""Set Value"", on_click=set_value(""42""), id=""set-value""),
             rx.text(""Loaded"", on_mount=on_load, id=""loaded""),
         )
 
@@ -98,13 +111,19 @@ def test_decentralized_event_handlers(
     assert decentralized_handlers.app_instance is not None
 
     counter = driver.find_element(By.ID, ""counter"")
+    value = driver.find_element(By.ID, ""value"")
     increment_button = driver.find_element(By.ID, ""increment"")
     reset_button = driver.find_element(By.ID, ""reset"")
+    set_value_button = driver.find_element(By.ID, ""set-value"")
 
     assert decentralized_handlers._poll_for(lambda: counter.text == ""10"", timeout=5)
+    assert value.text == ""0""
 
     increment_button.click()
     assert decentralized_handlers._poll_for(lambda: counter.text == ""11"", timeout=5)
 
     reset_button.click()
     assert decentralized_handlers._poll_for(lambda: counter.text == ""0"", timeout=5)
+
+    set_value_button.click()
+    assert decentralized_handlers._poll_for(lambda: value.text == ""42"", timeout=5)