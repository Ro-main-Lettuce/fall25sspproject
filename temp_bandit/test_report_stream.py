@@ -9,7 +9,6 @@
 from config_builder import ConfigBuilder
 
 from airbyte_cdk.models import SyncMode
-from airbyte_cdk.test.mock_http import HttpMocker
 
 
 class TestReportStream(BaseTest):
@@ -48,35 +47,28 @@ class TestSuiteReportStream(TestReportStream):
     cursor_field = ""TimePeriod""
 
     def setUp(self):
+        super().setUp()
         if not self.stream_name:
             self.skipTest(""Skipping TestSuiteReportStream"")
 
-    @HttpMocker()
-    def test_return_records_from_given_csv_file(self, http_mocker: HttpMocker):
-        self.auth_client(http_mocker)
+    def test_return_records_from_given_csv_file(self):
         output, _ = self.read_stream(self.stream_name, SyncMode.full_refresh, self._config, self.report_file)
         assert len(output.records) == self.records_number
 
-    @HttpMocker()
-    def test_transform_records_from_given_csv_file(self, http_mocker: HttpMocker):
-        self.auth_client(http_mocker)
+    def test_transform_records_from_given_csv_file(self):
         output, _ = self.read_stream(self.stream_name, SyncMode.full_refresh, self._config, self.report_file)
 
         assert len(output.records) == self.records_number
         for record in output.records:
             assert self.transform_field in record.record.data.keys()
 
-    @HttpMocker()
-    def test_incremental_read_returns_records(self, http_mocker: HttpMocker):
-        self.auth_client(http_mocker)
+    def test_incremental_read_returns_records(self):
         output, _ = self.read_stream(self.stream_name, SyncMode.incremental, self._config, self.report_file)
         assert len(output.records) == self.records_number
         assert output.most_recent_state.stream_state.__dict__ == self.first_read_state
 
-    @HttpMocker()
-    def test_incremental_read_with_state_returns_records(self, http_mocker: HttpMocker):
+    def test_incremental_read_with_state_returns_records(self):
         state = self._state(self.state_file, self.stream_name)
-        self.auth_client(http_mocker)
         output, service_call_mock = self.read_stream(
             self.stream_name, SyncMode.incremental, self._config, self.incremental_report_file, state
         )