@@ -77,11 +77,11 @@ def test_check(response, start_date, check_passed):
 @pytest.mark.parametrize(
     ""ticket_forms_response, status_code, expected_n_streams, expected_warnings, reason"",
     [
-        ('{""ticket_forms"": [{""id"": 1, ""updated_at"": ""2021-07-08T00:05:45Z""}]}', 200, 40, [], None),
+        ('{""ticket_forms"": [{""id"": 1, ""updated_at"": ""2021-07-08T00:05:45Z""}]}', 200, 41, [], None),
         (
             '{""error"": ""Not sufficient permissions""}',
             403,
-            37,
+            38,
             [
                 ""An exception occurred while trying to access TicketForms stream: Forbidden. You don't have permission to access this resource.. Skipping this stream.""
             ],
@@ -90,7 +90,7 @@ def test_check(response, start_date, check_passed):
         (
             """",
             404,
-            37,
+            38,
             [
                 ""An exception occurred while trying to access TicketForms stream: Not found. The requested resource was not found on the server.. Skipping this stream.""
             ],