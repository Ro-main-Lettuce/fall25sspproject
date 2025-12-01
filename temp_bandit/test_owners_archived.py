@@ -43,8 +43,8 @@ def response(self, with_pagination: bool = False):
     @HttpMocker()
     def test_given_one_page_when_read_stream_oauth_then_return_records(self, http_mocker: HttpMocker):
         self.mock_oauth(http_mocker, self.ACCESS_TOKEN)
-        self.mock_scopes(http_mocker, self.ACCESS_TOKEN, self.SCOPES)
         self.mock_custom_objects(http_mocker)
+        self.mock_dynamic_schema_requests(http_mocker)
         self.mock_response(http_mocker, self.request().build(), self.response().build())
         output = self.read_from_stream(self.oauth_config(), self.STREAM_NAME, SyncMode.full_refresh)
         assert len(output.records) == 1