@@ -1,6 +1,12 @@
 # Copyright (c) 2023 Airbyte, Inc., all rights reserved.
 
+from copy import deepcopy
+
+from freezegun import freeze_time
 from test_report_stream import TestSuiteReportStream
+from unit_tests.integrations.test_report_stream import MANIFEST_STREAMS
+
+from airbyte_cdk.models import SyncMode
 
 
 FIRST_STATE = {""180535609"": {""TimePeriod"": ""2023-11-12T00:00:00+00:00""}}
@@ -165,9 +171,63 @@ class TestAdGroupPerformanceReportHourlyStream(HourlyReportsTest):
     incremental_report_file = ""ad_group_performance_report_hourly_incremental""
 
 
-class TestAccountPerformanceReportHourlyStream(HourlyReportsTest):
+class TestAccountPerformanceReportHourlyStream(HourlyReportsTestWithStateChangesAfterMigration):
     stream_name = ""account_performance_report_hourly""
     report_file = ""account_performance_report_hourly""
     records_number = 24
     state_file = ""hourly_reports_state""
     incremental_report_file = ""account_performance_report_hourly_incremental""
+    report_file_with_records_further_start_date = ""account_performance_report_hourly_with_records_further_config_start_date""
+    state_file_legacy = ""hourly_reports_state_legacy""
+    state_file_after_migration = ""hourly_reports_state_after_migration""
+    state_file_after_migration_with_cursor_further_config_start_date = (
+        ""hourly_reports_state_after_migration_with_cursor_further_config_start_date""
+    )
+    incremental_report_file_with_records_further_cursor = ""account_performance_report_hourly_incremental_with_records_further_cursor""
+
+    def mock_report_apis(self):
+        self.mock_user_query_api(response_template=""user_query"")
+        self.mock_accounts_search_api(
+            response_template=""accounts_search_for_report"",
+            body=b'{""PageInfo"": {""Index"": 0, ""Size"": 1000}, ""Predicates"": [{""Field"": ""UserId"", ""Operator"": ""Equals"", ""Value"": ""123456789""}], ""ReturnAdditionalFields"": ""TaxCertificate,AccountMode""}',
+        )
+        self.mock_generate_report_api(
+            endpoint=""Submit"",
+            response_template=""generate_report"",
+            body=b'{""ReportRequest"": {""ExcludeColumnHeaders"": false, ""ExcludeReportFooter"": true, ""ExcludeReportHeader"": true, ""Format"": ""Csv"", ""FormatVersion"": ""2.0"", ""ReportName"": ""AccountPerformanceReport"", ""ReturnOnlyCompleteData"": false, ""Type"": ""AccountPerformanceReportRequest"", ""Aggregation"": ""Hourly"", ""Columns"": [""AccountId"", ""TimePeriod"", ""CurrencyCode"", ""AdDistribution"", ""DeviceType"", ""Network"", ""DeliveredMatchType"", ""DeviceOS"", ""TopVsOther"", ""BidMatchType"", ""AccountName"", ""AccountNumber"", ""PhoneImpressions"", ""PhoneCalls"", ""Clicks"", ""Ctr"", ""Spend"", ""Impressions"", ""Assists"", ""ReturnOnAdSpend"", ""AverageCpc"", ""AveragePosition"", ""AverageCpm"", ""Conversions"", ""ConversionsQualified"", ""ConversionRate"", ""CostPerAssist"", ""CostPerConversion"", ""LowQualityClicks"", ""LowQualityClicksPercent"", ""LowQualityImpressions"", ""LowQualitySophisticatedClicks"", ""LowQualityConversions"", ""LowQualityConversionRate"", ""Revenue"", ""RevenuePerAssist"", ""RevenuePerConversion"", ""Ptr""], ""Scope"": {""AccountIds"": [180535609]}, ""Time"": {""CustomDateRangeStart"": {""Day"": 1, ""Month"": 1, ""Year"": 2024}, ""CustomDateRangeEnd"": {""Day"": 6, ""Month"": 5, ""Year"": 2024}, ""ReportTimeZone"": ""GreenwichMeanTimeDublinEdinburghLisbonLondon""}}}',
+        )
+        # for second read
+        self.mock_generate_report_api(
+            endpoint=""Submit"",
+            response_template=""generate_report"",
+            body=b'{""ReportRequest"": {""ExcludeColumnHeaders"": false, ""ExcludeReportFooter"": true, ""ExcludeReportHeader"": true, ""Format"": ""Csv"", ""FormatVersion"": ""2.0"", ""ReportName"": ""AccountPerformanceReport"", ""ReturnOnlyCompleteData"": false, ""Type"": ""AccountPerformanceReportRequest"", ""Aggregation"": ""Hourly"", ""Columns"": [""AccountId"", ""TimePeriod"", ""CurrencyCode"", ""AdDistribution"", ""DeviceType"", ""Network"", ""DeliveredMatchType"", ""DeviceOS"", ""TopVsOther"", ""BidMatchType"", ""AccountName"", ""AccountNumber"", ""PhoneImpressions"", ""PhoneCalls"", ""Clicks"", ""Ctr"", ""Spend"", ""Impressions"", ""Assists"", ""ReturnOnAdSpend"", ""AverageCpc"", ""AveragePosition"", ""AverageCpm"", ""Conversions"", ""ConversionsQualified"", ""ConversionRate"", ""CostPerAssist"", ""CostPerConversion"", ""LowQualityClicks"", ""LowQualityClicksPercent"", ""LowQualityImpressions"", ""LowQualitySophisticatedClicks"", ""LowQualityConversions"", ""LowQualityConversionRate"", ""Revenue"", ""RevenuePerAssist"", ""RevenuePerConversion"", ""Ptr""], ""Scope"": {""AccountIds"": [180535609]}, ""Time"": {""CustomDateRangeStart"": {""Day"": 6, ""Month"": 5, ""Year"": 2024}, ""CustomDateRangeEnd"": {""Day"": 8, ""Month"": 5, ""Year"": 2024}, ""ReportTimeZone"": ""GreenwichMeanTimeDublinEdinburghLisbonLondon""}}}',
+        )
+        self.mock_generate_report_api(
+            endpoint=""Poll"", response_template=""generate_report_poll"", body=b'{""ReportRequestId"": ""thisisthereport_requestid""}'
+        )
+
+    @freeze_time(""2024-05-06"")
+    def test_no_config_start_date(self):
+        """"""
+        If the field reports_start_date is blank, Airbyte will replicate all data from previous and current calendar years.
+        This test is to validate that the stream will return all records from the first day of the year 2023 (CustomDateRangeStart in mocked body).
+        """"""
+        if self.stream_name not in MANIFEST_STREAMS:
+            self.skipTest(f""Skipping for NOT migrated to manifest stream: {self.stream_name}"")
+        self.mock_report_apis()
+        # here we mock the report start date to be the first day of the year 2023
+        self.mock_generate_report_api(
+            endpoint=""Submit"",
+            response_template=""generate_report"",
+            body=b'{""ReportRequest"": {""ExcludeColumnHeaders"": false, ""ExcludeReportFooter"": true, ""ExcludeReportHeader"": true, ""Format"": ""Csv"", ""FormatVersion"": ""2.0"", ""ReportName"": ""AccountPerformanceReport"", ""ReturnOnlyCompleteData"": false, ""Type"": ""AccountPerformanceReportRequest"", ""Aggregation"": ""Hourly"", ""Columns"": [""AccountId"", ""TimePeriod"", ""CurrencyCode"", ""AdDistribution"", ""DeviceType"", ""Network"", ""DeliveredMatchType"", ""DeviceOS"", ""TopVsOther"", ""BidMatchType"", ""AccountName"", ""AccountNumber"", ""PhoneImpressions"", ""PhoneCalls"", ""Clicks"", ""Ctr"", ""Spend"", ""Impressions"", ""Assists"", ""ReturnOnAdSpend"", ""AverageCpc"", ""AveragePosition"", ""AverageCpm"", ""Conversions"", ""ConversionsQualified"", ""ConversionRate"", ""CostPerAssist"", ""CostPerConversion"", ""LowQualityClicks"", ""LowQualityClicksPercent"", ""LowQualityImpressions"", ""LowQualitySophisticatedClicks"", ""LowQualityConversions"", ""LowQualityConversionRate"", ""Revenue"", ""RevenuePerAssist"", ""RevenuePerConversion"", ""Ptr""], ""Scope"": {""AccountIds"": [180535609]}, ""Time"": {""CustomDateRangeStart"": {""Day"": 1, ""Month"": 1, ""Year"": 2023}, ""CustomDateRangeEnd"": {""Day"": 6, ""Month"": 5, ""Year"": 2024}, ""ReportTimeZone"": ""GreenwichMeanTimeDublinEdinburghLisbonLondon""}}}',
+        )
+        config = deepcopy(self._config)
+        del config[""reports_start_date""]
+        output, _ = self.read_stream(self.stream_name, SyncMode.incremental, config, self.report_file)
+        assert len(output.records) == self.records_number
+        first_read_state = deepcopy(self.first_read_state)
+        # this corresponds to the last read record as we don't have started_date in the config
+        # the self.first_read_state is set using the config start date so it is not correct for this test
+        first_read_state[""state""][self.cursor_field] = ""2023-11-12T00:00:00+00:00""
+        first_read_state[""states""][0][""cursor""][self.cursor_field] = ""2023-11-12T00:00:00+00:00""
+        assert output.most_recent_state.stream_state.__dict__ == first_read_state