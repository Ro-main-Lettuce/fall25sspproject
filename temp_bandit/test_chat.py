@@ -233,10 +233,7 @@ def mock_model(
         ChatMessage(role=""assistant"", content=""Hi there!""),
     ]
 
-    # Simulate clearing messages
-    chat._value = []
-    assert chat.value == []
-    assert chat._chat_history == []
+    assert chat._convert_value({""messages"": []}) == []
 
 
 async def test_chat_send_message_enqueues_ui_element_request(