@@ -153,13 +153,13 @@ async def get_state_text():
     # clear the input on the backend
     clear_text_backend = driver.find_element(By.ID, ""clear-text-backend"")
     clear_text_backend.click()
-    assert await get_state_text() == """"
     assert (
         fully_controlled_input.poll_for_value(
             debounce_input, exp_not_equal=""ifoonitial""
         )
         == """"
     )
+    assert await get_state_text() == """"
 
     # type more characters
     debounce_input.send_keys(""getting testing done"")