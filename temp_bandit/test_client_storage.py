@@ -4,6 +4,7 @@
 
 import asyncio
 from collections.abc import Generator
+from pathlib import Path
 
 import pytest
 from selenium.webdriver import Firefox
@@ -39,6 +40,11 @@ def set_state_var(self, value: str):
         def set_input_value(self, value: str):
             self.input_value = value
 
+        @rx.event
+        async def do_reset(self):
+            root_state = await self.get_state(rx.State)
+            root_state.reset()
+
     class ClientSideSubState(ClientSideState):
         # cookies with default settings
         c1: str = rx.Cookie()
@@ -93,6 +99,9 @@ def index():
                 read_only=True,
                 id=""token"",
             ),
+            rx.button(
+                ""State Reset"", on_click=ClientSideState.do_reset, id=""reset-button""
+            ),
             rx.input(
                 placeholder=""state var"",
                 value=ClientSideState.state_var,
@@ -238,6 +247,7 @@ async def test_client_side_state(
     driver: WebDriver,
     local_storage: utils.LocalStorage,
     session_storage: utils.SessionStorage,
+    tmp_path: Path,
 ):
     """"""Test client side state.
 
@@ -246,6 +256,7 @@ async def test_client_side_state(
         driver: WebDriver instance.
         local_storage: Local storage helper.
         session_storage: Session storage helper.
+        tmp_path: pytest tmp_path fixture
     """"""
     app = client_side.app_instance
     assert app is not None
@@ -535,8 +546,8 @@ def set_sub_sub(var: str, value: str):
     assert s1s.text == ""s1s value""
 
     # reset the backend state to force refresh from client storage
-    async with client_side.modify_state(f""{token}_{state_name}"") as state:
-        state.reset()
+    reset_button = driver.find_element(By.ID, ""reset-button"")
+    reset_button.click()
     driver.refresh()
 
     # wait for the backend connection to send the token (again)
@@ -652,7 +663,7 @@ def set_sub_sub(var: str, value: str):
             _substate_key(token, sub_sub_state_name)
         )
     elif isinstance(client_side.state_manager, (StateManagerMemory, StateManagerDisk)):
-        del client_side.state_manager.states[token]
+        client_side.state_manager.states.pop(token, None)
     if isinstance(client_side.state_manager, StateManagerDisk):
         client_side.state_manager.token_expiration = 0
         client_side.state_manager._purge_expired_states()
@@ -666,6 +677,7 @@ async def poll_for_not_hydrated():
 
     # Trigger event to get a new instance of the state since the old was expired.
     set_sub(""c1"", ""c1 post expire"")
+    set_sub_sub(""s1s"", ""s1s post expire"")
 
     # get new references to all cookie and local storage elements (again)
     c1 = driver.find_element(By.ID, ""c1"")
@@ -702,7 +714,7 @@ async def poll_for_not_hydrated():
     assert s3.text == ""s3 value""
     assert c1s.text == ""c1s value""
     assert l1s.text == ""l1s value""
-    assert s1s.text == ""s1s value""
+    assert s1s.text == ""s1s post expire""
 
     # Get the backend state and ensure the values are still set
     async def get_sub_state():
@@ -712,11 +724,20 @@ async def get_sub_state():
         state = root_state.substates[client_side.get_state_name(""_client_side_state"")]
         return state.substates[client_side.get_state_name(""_client_side_sub_state"")]
 
-    async def poll_for_c1_set():
+    async def get_sub_sub_state():
+        sub_state = await get_sub_state()
+        return sub_state.substates[
+            client_side.get_state_name(""_client_side_sub_sub_state"")
+        ]
+
+    async def poll_for_post_expire_set():
         sub_state = await get_sub_state()
-        return sub_state.c1 == ""c1 post expire""
+        sub_sub_state = await get_sub_sub_state()
+        return (
+            sub_state.c1 == ""c1 post expire"" and sub_sub_state.s1s == ""s1s post expire""
+        )
 
-    assert await AppHarness._poll_for_async(poll_for_c1_set)
+    assert await AppHarness._poll_for_async(poll_for_post_expire_set)
     sub_state = await get_sub_state()
     assert sub_state.c1 == ""c1 post expire""
     assert sub_state.c2 == ""c2 value""
@@ -732,12 +753,10 @@ async def poll_for_c1_set():
     assert sub_state.s1 == ""s1 value""
     assert sub_state.s2 == ""s2 value""
     assert sub_state.s3 == ""s3 value""
-    sub_sub_state = sub_state.substates[
-        client_side.get_state_name(""_client_side_sub_sub_state"")
-    ]
+    sub_sub_state = await get_sub_sub_state()
     assert sub_sub_state.c1s == ""c1s value""
     assert sub_sub_state.l1s == ""l1s value""
-    assert sub_sub_state.s1s == ""s1s value""
+    assert sub_sub_state.s1s == ""s1s post expire""
 
     # clear the cookie jar and local storage, ensure state reset to default
     driver.delete_all_cookies()