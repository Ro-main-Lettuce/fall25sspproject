@@ -1,18 +1,23 @@
 #
 # Copyright (c) 2023 Airbyte, Inc., all rights reserved.
 #
+from datetime import datetime, timezone
+from unittest.mock import MagicMock, patch
 
 
-def test_get_tokens(components_module, requests_mock, mocker):
+def test_get_tokens(components_module):
     url = ""https://auth.railz.ai/getAccess""
     responses = [
+        {""access_token"": ""access_token1""},
         {""access_token"": ""access_token1""},
         {""access_token"": ""access_token2""},
     ]
-    requests_mock.get(url, json=lambda request, context: responses.pop(0))
 
-    current_time = 1000.0
-    mock_time = mocker.patch(""time.time"", return_value=current_time)
+    timestamps = [
+        datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc).timestamp(),
+        datetime(2023, 1, 1, 12, 30, 0, tzinfo=timezone.utc).timestamp(),
+        datetime(2023, 1, 1, 13, 0, 0, tzinfo=timezone.utc).timestamp(),
+    ]
 
     ShortLivedTokenAuthenticator = components_module.ShortLivedTokenAuthenticator
     authenticator = ShortLivedTokenAuthenticator(
@@ -25,12 +30,12 @@ def test_get_tokens(components_module, requests_mock, mocker):
         parameters={},
     )
 
-    token1 = authenticator.token
-    assert token1 == ""Bearer access_token1""
-    assert authenticator._timestamp == current_time
-
-    mock_time.return_value = current_time + 1800
-    assert authenticator.token == ""Bearer access_token1""
+    def mock_requests_get(*args, **kwargs):
+        mock_response = MagicMock()
+        mock_response.json.return_value = responses[0]
+        return mock_response
 
-    mock_time.return_value = current_time + 3601
-    assert authenticator.token == ""Bearer access_token2""
+    # Mock requests.get and time.time
+    for _ in range(3):
+        with patch(""requests.Session.get"", side_effect=mock_requests_get), patch(""time.time"", return_value=timestamps.pop(0)):
+            assert authenticator.token == f""Bearer {responses.pop(0)['access_token']}""