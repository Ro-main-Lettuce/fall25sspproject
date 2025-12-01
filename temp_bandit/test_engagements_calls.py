@@ -10,7 +10,7 @@
 from airbyte_cdk.test.mock_http import HttpMocker, HttpResponse
 from airbyte_cdk.test.mock_http.response_builder import FieldPath
 
-from . import HubspotTestCase
+from . import OBJECTS_WITH_DYNAMIC_SCHEMA, HubspotTestCase
 from .request_builders.streams import CRMStreamRequestBuilder
 from .response_builder.streams import HubspotStreamResponseBuilder
 
@@ -51,7 +51,6 @@ def response(self, with_pagination: bool = False):
 
     def _set_up_oauth(self, http_mocker: HttpMocker):
         self.mock_oauth(http_mocker, self.ACCESS_TOKEN)
-        self.mock_scopes(http_mocker, self.ACCESS_TOKEN, self.SCOPES)
 
     def _set_up_requests(
         self, http_mocker: HttpMocker, with_oauth: bool = False, with_dynamic_schemas: bool = True, entities: Optional[List[str]] = None
@@ -69,8 +68,9 @@ def test_given_oauth_authentication_when_read_then_perform_authenticated_queries
             http_mocker,
             with_oauth=True,
             with_dynamic_schemas=True,
-            entities=[""calls"", ""company"", ""contact"", ""emails"", ""meetings"", ""notes"", ""tasks""],
+            entities=OBJECTS_WITH_DYNAMIC_SCHEMA,
         )
+        self.mock_response(http_mocker, self.request(), self.response())
         self.read_from_stream(self.oauth_config(), self.STREAM_NAME, SyncMode.full_refresh)
 
     @HttpMocker()
@@ -79,7 +79,7 @@ def test_given_records_when_read_extract_desired_records(self, http_mocker: Http
             http_mocker,
             with_oauth=True,
             with_dynamic_schemas=True,
-            entities=[""calls"", ""company"", ""contact"", ""emails"", ""leads"", ""meetings"", ""notes"", ""tasks""],
+            entities=OBJECTS_WITH_DYNAMIC_SCHEMA,
         )
         self.mock_response(http_mocker, self.request(), self.response())
         output = self.read_from_stream(self.oauth_config(), self.STREAM_NAME, SyncMode.full_refresh)
@@ -123,7 +123,6 @@ def test_given_500_then_200_when_read_then_return_records(self, http_mocker: Htt
     @HttpMocker()
     def test_given_missing_scopes_error_when_read_then_stop_sync(self, http_mocker: HttpMocker):
         self.mock_oauth(http_mocker, self.ACCESS_TOKEN)
-        self.mock_scopes(http_mocker, self.ACCESS_TOKEN, [])
         self.mock_custom_objects_streams(http_mocker)
         self.read_from_stream(self.oauth_config(), self.STREAM_NAME, SyncMode.full_refresh, expecting_exception=True)
 