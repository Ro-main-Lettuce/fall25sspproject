@@ -80,7 +80,7 @@ def test_message_endpoint(
     # Test data
     request_data = {
         ""allMessages"": [{""role"": ""user"", ""content"": ""Build me an app to plan my meals""}],
-        ""chatbotId"": ""test-bot-id"",
+        ""applicationId"": ""test-bot-id"",
         ""traceId"": ""test-trace-id"",
         ""settings"": {""max-iterations"": 3}
     }
@@ -132,7 +132,7 @@ def test_message_endpoint_error_handling(
         # Test data
         request_data = {
             ""allMessages"": [{""role"": ""user"", ""content"": ""Build me an app to plan my meals""}],
-            ""chatbotId"": ""test-bot-id"",
+            ""applicationId"": ""test-bot-id"",
             ""traceId"": ""test-trace-id"",
             ""settings"": {""max-iterations"": 3}
         }
@@ -154,7 +154,7 @@ def test_multiple_sse_updates(
     # Test data
     request_data = {
         ""allMessages"": [{""role"": ""user"", ""content"": ""Build me an app with multiple steps""}],
-        ""chatbotId"": ""test-bot-id"",
+        ""applicationId"": ""test-bot-id"",
         ""traceId"": ""test-trace-id"",
         ""settings"": {""max-iterations"": 3}
     }
@@ -232,7 +232,7 @@ def test_different_message_kinds(
     # Test data
     request_data = {
         ""allMessages"": [{""role"": ""user"", ""content"": ""Build me an app with feedback""}],
-        ""chatbotId"": ""test-bot-id"",
+        ""applicationId"": ""test-bot-id"",
         ""traceId"": ""test-trace-id"",
         ""settings"": {""max-iterations"": 3}
     }
@@ -299,4 +299,4 @@ def test_different_message_kinds(
                 message_kinds = [event[""message""][""kind""] for event in events if ""message"" in event]
                 assert MessageKind.STAGE_RESULT.value in message_kinds
                 assert MessageKind.FEEDBACK_RESPONSE.value in message_kinds
-                assert MessageKind.RUNTIME_ERROR.value in message_kinds
\ No newline at end of file
+                assert MessageKind.RUNTIME_ERROR.value in message_kinds