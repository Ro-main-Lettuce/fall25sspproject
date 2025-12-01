@@ -51,7 +51,6 @@ def response(self, with_pagination: bool = False):
 
     def _set_up_oauth(self, http_mocker: HttpMocker):
         self.mock_oauth(http_mocker, self.ACCESS_TOKEN)
-        self.mock_scopes(http_mocker, self.ACCESS_TOKEN, self.SCOPES)
 
     def _set_up_requests(self, http_mocker: HttpMocker, with_oauth: bool = False, with_dynamic_schema: bool = True):
         if with_oauth:
@@ -63,12 +62,12 @@ def _set_up_requests(self, http_mocker: HttpMocker, with_oauth: bool = False, wi
 
     @HttpMocker()
     def test_given_oauth_authentication_when_read_then_perform_authenticated_queries(self, http_mocker: HttpMocker):
-        self._set_up_requests(http_mocker, with_oauth=True, with_dynamic_schema=False)
+        self._set_up_requests(http_mocker, with_oauth=True, with_dynamic_schema=True)
         self.read_from_stream(self.oauth_config(), self.STREAM_NAME, SyncMode.full_refresh)
 
     @HttpMocker()
     def test_given_records_when_read_extract_desired_records(self, http_mocker: HttpMocker):
-        self._set_up_requests(http_mocker, with_oauth=True, with_dynamic_schema=False)
+        self._set_up_requests(http_mocker, with_oauth=True, with_dynamic_schema=True)
         self.mock_response(http_mocker, self.request(), self.response())
         output = self.read_from_stream(self.oauth_config(), self.STREAM_NAME, SyncMode.full_refresh)
         assert len(output.records) == 1
@@ -111,7 +110,6 @@ def test_given_500_then_200_when_read_then_return_records(self, http_mocker: Htt
     @HttpMocker()
     def test_given_missing_scopes_error_when_read_then_stop_sync(self, http_mocker: HttpMocker):
         self.mock_oauth(http_mocker, self.ACCESS_TOKEN)
-        self.mock_scopes(http_mocker, self.ACCESS_TOKEN, [])
         self.mock_custom_objects_streams(http_mocker)
         self.read_from_stream(self.oauth_config(), self.STREAM_NAME, SyncMode.full_refresh, expecting_exception=True)
 