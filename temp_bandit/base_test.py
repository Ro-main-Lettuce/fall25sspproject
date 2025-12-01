@@ -7,20 +7,29 @@
 
 from bingads.v13.bulk import BulkServiceManager
 from bingads.v13.reporting.reporting_service_manager import ReportingServiceManager
-from client_builder import build_request, response_with_status
+from client_builder import build_request, build_request_2, response_with_status
 from config_builder import ConfigBuilder
-from source_bing_ads.source import SourceBingAds
+from protocol_helpers import read_helper
 from suds.transport.https import HttpAuthenticated
 from suds_response_mock import mock_http_authenticated_send
 
-from airbyte_cdk.models import AirbyteStateMessage, SyncMode
+from airbyte_cdk.models import AirbyteLogMessage, AirbyteMessage, AirbyteStateMessage, Level, SyncMode, Type
 from airbyte_cdk.test.catalog_builder import CatalogBuilder
 from airbyte_cdk.test.entrypoint_wrapper import EntrypointOutput, read
 from airbyte_cdk.test.mock_http import HttpMocker
 from airbyte_cdk.test.state_builder import StateBuilder
 
 
 class BaseTest(TestCase):
+    def setUp(self) -> None:
+        self._http_mocker = HttpMocker()
+        self._http_mocker.__enter__()
+
+        self._auth_client(self._http_mocker)
+
+    def tearDown(self) -> None:
+        self._http_mocker.__exit__(None, None, None)
+
     @property
     def service_manager(self) -> Union[ReportingServiceManager, BulkServiceManager]:
         pass
@@ -38,8 +47,9 @@ def _state(self, file: str, stream_name: str) -> list[AirbyteStateMessage]:
             state = json.loads(f.read())
             return StateBuilder().with_stream_state(stream_name, state).build()
 
-    def auth_client(self, http_mocker: HttpMocker) -> None:
+    def _auth_client(self, http_mocker: HttpMocker) -> None:
         http_mocker.post(request=build_request(self._config), responses=response_with_status(""oauth"", 200))
+        http_mocker.post(request=build_request_2(self._config), responses=response_with_status(""oauth"", 200))
 
     def read_stream(
         self,
@@ -55,4 +65,18 @@ def read_stream(
                 self.service_manager, ""download_file"", return_value=self._download_file(stream_data_file)
             ) as service_call_mock:
                 catalog = CatalogBuilder().with_stream(stream_name, sync_mode).build()
-                return read(SourceBingAds(), config, catalog, state, expecting_exception), service_call_mock
+                return read_helper(config, catalog, state, expecting_exception), service_call_mock
+
+    @property
+    def http_mocker(self) -> HttpMocker:
+        return self._http_mocker
+
+    @staticmethod
+    def create_log_message(log_message: str):
+        return AirbyteMessage(
+            type=Type.LOG,
+            log=AirbyteLogMessage(
+                level=Level.INFO,
+                message=log_message,
+            ),
+        )