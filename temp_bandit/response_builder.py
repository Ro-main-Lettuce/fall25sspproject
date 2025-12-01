@@ -24,6 +24,6 @@ def build_response(
 def get_account_response() -> HttpResponse:
     response = {
         ""data"": [{""id"": PAGE_ID, ""name"": ""AccountName"", ""instagram_business_account"": {""id"": BUSINESS_ACCOUNT_ID}}],
-        ""paging"": {""cursors"": {""before"": ""before_token"", ""after"": ""after_token""}},
+        ""paging"": {""cursors"": {""before"": ""before_token""}},
     }
     return build_response(body=response, status_code=HTTPStatus.OK)