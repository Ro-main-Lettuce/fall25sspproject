@@ -9,16 +9,17 @@
 from typing import List, Optional
 
 import freezegun
+import pendulum
 import pytest
 import requests_mock
 from source_amazon_seller_partner.streams import ReportProcessingStatus
 
+from airbyte_cdk.models import AirbyteStateMessage, FailureType, Level, SyncMode
 from airbyte_cdk.test.entrypoint_wrapper import EntrypointOutput
 from airbyte_cdk.test.mock_http import HttpMocker, HttpResponse
 from airbyte_cdk.test.mock_http.matcher import HttpRequestMatcher
-from airbyte_protocol.models import AirbyteStateMessage, FailureType, SyncMode
 
-from .config import CONFIG_END_DATE, CONFIG_START_DATE, MARKETPLACE_ID, NOW, VENDOR_TRAFFIC_REPORT_CONFIG_END_DATE, ConfigBuilder
+from .config import CONFIG_END_DATE, CONFIG_START_DATE, MARKETPLACE_ID, NOW, ConfigBuilder
 from .request_builder import RequestBuilder
 from .response_builder import build_response, response_with_status
 from .utils import assert_message_in_log_output, config, find_template, get_stream_by_name, mock_auth, read_output
@@ -40,28 +41,20 @@
     (""GET_LEDGER_DETAIL_VIEW_DATA"", ""csv""),
     (""GET_AFN_INVENTORY_DATA_BY_COUNTRY"", ""csv""),
     (""GET_FLAT_FILE_RETURNS_DATA_BY_RETURN_DATE"", ""csv""),
-    (""GET_VENDOR_SALES_REPORT"", ""json""),
-    (""GET_BRAND_ANALYTICS_MARKET_BASKET_REPORT"", ""json""),
     (""GET_FBA_FULFILLMENT_CUSTOMER_RETURNS_DATA"", ""csv""),
     (""GET_FBA_SNS_FORECAST_DATA"", ""csv""),
     (""GET_AFN_INVENTORY_DATA"", ""csv""),
     (""GET_MERCHANT_CANCELLED_LISTINGS_DATA"", ""csv""),
     (""GET_FBA_FULFILLMENT_CUSTOMER_SHIPMENT_PROMOTION_DATA"", ""csv""),
     (""GET_LEDGER_SUMMARY_VIEW_DATA"", ""csv""),
-    (""GET_BRAND_ANALYTICS_SEARCH_TERMS_REPORT"", ""json""),
-    (""GET_BRAND_ANALYTICS_REPEAT_PURCHASE_REPORT"", ""json""),
     (""GET_FLAT_FILE_ARCHIVED_ORDERS_DATA_BY_ORDER_DATE"", ""csv""),
-    (""GET_VENDOR_INVENTORY_REPORT"", ""json""),
     (""GET_FBA_SNS_PERFORMANCE_DATA"", ""csv""),
     (""GET_FBA_ESTIMATED_FBA_FEES_TXT_DATA"", ""csv""),
     (""GET_FBA_INVENTORY_PLANNING_DATA"", ""csv""),
     (""GET_FBA_STORAGE_FEE_CHARGES_DATA"", ""csv""),
     (""GET_FBA_MYI_UNSUPPRESSED_INVENTORY_DATA"", ""csv""),
     (""GET_STRANDED_INVENTORY_UI_DATA"", ""csv""),
     (""GET_FBA_REIMBURSEMENTS_DATA"", ""csv""),
-    (""GET_VENDOR_NET_PURE_PRODUCT_MARGIN_REPORT"", ""json""),
-    (""GET_VENDOR_REAL_TIME_INVENTORY_REPORT"", ""json""),
-    (""GET_VENDOR_TRAFFIC_REPORT"", ""json""),
 )
 
 
@@ -70,8 +63,6 @@ def _create_report_request(report_name: str) -> RequestBuilder:
     A POST request needed to start generating a report on Amazon SP platform.
     Performed in ReportsAmazonSPStream._create_report method.
     """"""
-    if report_name == ""GET_VENDOR_TRAFFIC_REPORT"":
-        return RequestBuilder.create_vendor_traffic_report_endpoint(report_name)
     return RequestBuilder.create_report_endpoint(report_name)
 
 
@@ -173,6 +164,7 @@ def _read(stream_name: str, config_: ConfigBuilder, expecting_exception: bool =
     @pytest.mark.parametrize((""stream_name"", ""data_format""), STREAMS)
     @HttpMocker()
     def test_given_report_when_read_then_return_records(self, stream_name: str, data_format: str, http_mocker: HttpMocker) -> None:
+        http_mocker.clear_all_matchers()
         mock_auth(http_mocker)
         http_mocker.post(_create_report_request(stream_name).build(), _create_report_response(_REPORT_ID))
         http_mocker.get(
@@ -196,6 +188,7 @@ def test_given_report_when_read_then_return_records(self, stream_name: str, data
     def test_given_compressed_report_when_read_then_return_records(
         self, stream_name: str, data_format: str, http_mocker: HttpMocker
     ) -> None:
+        http_mocker.clear_all_matchers()
         mock_auth(http_mocker)
         http_mocker.post(_create_report_request(stream_name).build(), _create_report_response(_REPORT_ID))
         http_mocker.get(
@@ -227,6 +220,7 @@ def test_given_compressed_report_when_read_then_return_records(
     def test_given_http_status_500_then_200_when_create_report_then_retry_and_return_records(
         self, stream_name: str, data_format: str, http_mocker: HttpMocker
     ) -> None:
+        http_mocker.clear_all_matchers()
         mock_auth(http_mocker)
         http_mocker.post(
             _create_report_request(stream_name).build(),
@@ -253,6 +247,7 @@ def test_given_http_status_500_then_200_when_create_report_then_retry_and_return
     def test_given_http_status_500_then_200_when_retrieve_report_then_retry_and_return_records(
         self, stream_name: str, data_format: str, http_mocker: HttpMocker
     ) -> None:
+        http_mocker.clear_all_matchers()
         mock_auth(http_mocker)
         http_mocker.post(_create_report_request(stream_name).build(), _create_report_response(_REPORT_ID))
         http_mocker.get(
@@ -279,6 +274,7 @@ def test_given_http_status_500_then_200_when_retrieve_report_then_retry_and_retu
     def test_given_http_status_500_then_200_when_get_document_url_then_retry_and_return_records(
         self, stream_name: str, data_format: str, http_mocker: HttpMocker
     ) -> None:
+        http_mocker.clear_all_matchers()
         mock_auth(http_mocker)
         http_mocker.post(_create_report_request(stream_name).build(), _create_report_response(_REPORT_ID))
         http_mocker.get(
@@ -305,6 +301,7 @@ def test_given_http_status_500_then_200_when_get_document_url_then_retry_and_ret
     def test_given_http_status_500_then_200_when_download_document_then_retry_and_return_records(
         self, stream_name: str, data_format: str, http_mocker: HttpMocker
     ) -> None:
+        http_mocker.clear_all_matchers()
         mock_auth(http_mocker)
         http_mocker.post(_create_report_request(stream_name).build(), _create_report_response(_REPORT_ID))
         http_mocker.get(
@@ -331,15 +328,13 @@ def test_given_http_status_500_then_200_when_download_document_then_retry_and_re
     def test_given_report_access_forbidden_when_read_then_no_records_and_error_logged(
         self, stream_name: str, data_format: str, http_mocker: HttpMocker
     ) -> None:
+        http_mocker.clear_all_matchers()
         mock_auth(http_mocker)
 
         http_mocker.post(_create_report_request(stream_name).build(), response_with_status(status_code=HTTPStatus.FORBIDDEN))
 
         output = self._read(stream_name, config())
-        message_on_access_forbidden = (
-            ""This is most likely due to insufficient permissions on the credentials in use. ""
-            ""Try to grant required permissions/scopes or re-authenticate.""
-        )
+        message_on_access_forbidden = ""Forbidden. You don't have permission to access this resource.""
         assert output.errors[0].trace.error.failure_type == FailureType.config_error
         assert message_on_access_forbidden in output.errors[0].trace.error.message
 
@@ -348,6 +343,7 @@ def test_given_report_access_forbidden_when_read_then_no_records_and_error_logge
     def test_given_report_status_cancelled_when_read_then_stream_completed_successfully_and_warn_about_cancellation(
         self, stream_name: str, data_format: str, http_mocker: HttpMocker
     ) -> None:
+        http_mocker.clear_all_matchers()
         mock_auth(http_mocker)
 
         http_mocker.post(_create_report_request(stream_name).build(), _create_report_response(_REPORT_ID))
@@ -356,17 +352,18 @@ def test_given_report_status_cancelled_when_read_then_stream_completed_successfu
             _check_report_status_response(stream_name, processing_status=ReportProcessingStatus.CANCELLED),
         )
 
-        message_on_report_cancelled = f""The report for stream '{stream_name}' was cancelled or there is no data to return.""
+        message_on_report_cancelled = f""Exception while syncing stream {stream_name}""
 
         output = self._read(stream_name, config())
-        assert_message_in_log_output(message_on_report_cancelled, output)
+        assert_message_in_log_output(message=message_on_report_cancelled, entrypoint_output=output, log_level=Level.ERROR)
         assert len(output.records) == 0
 
     @pytest.mark.parametrize((""stream_name"", ""data_format""), STREAMS)
     @HttpMocker()
     def test_given_report_status_fatal_when_read_then_exception_raised(
         self, stream_name: str, data_format: str, http_mocker: HttpMocker
     ) -> None:
+        http_mocker.clear_all_matchers()
         mock_auth(http_mocker)
 
         http_mocker.post(_create_report_request(stream_name).build(), _create_report_response(_REPORT_ID))
@@ -377,39 +374,26 @@ def test_given_report_status_fatal_when_read_then_exception_raised(
             ),
         )
 
-        http_mocker.get(
-            _get_document_download_url_request(_REPORT_DOCUMENT_ID).build(),
-            _get_document_download_url_response(_DOCUMENT_DOWNLOAD_URL, _REPORT_DOCUMENT_ID),
-        )
-        http_mocker.get(
-            _download_document_request(_DOCUMENT_DOWNLOAD_URL).build(),
-            [
-                response_with_status(status_code=HTTPStatus.INTERNAL_SERVER_ERROR),
-                _download_document_error_response(),
-            ],
-        )
-
         output = self._read(stream_name, config(), expecting_exception=True)
         assert output.errors[-1].trace.error.failure_type == FailureType.config_error
         config_end_date = CONFIG_END_DATE
-        if stream_name == ""GET_VENDOR_TRAFFIC_REPORT"":
-            config_end_date = VENDOR_TRAFFIC_REPORT_CONFIG_END_DATE
         assert (
-            f""Failed to retrieve the report '{stream_name}' for period {CONFIG_START_DATE}-{config_end_date}. This will be read during the next sync. Report ID: 6789087632. Error: {{'errorDetails': 'Error in report request: This report type requires the reportPeriod, distributorView, sellingProgram reportOption to be specified. Please review the document for this report type on GitHub, provide a value for this reportOption in your request, and try again.'}}""
+            f""At least one job could not be completed for slice {{\\'start_time\\': \\'{CONFIG_START_DATE}\\', \\'end_time\\': \\'{config_end_date}\\'}}""
         ) in output.errors[-1].trace.error.message
 
     @pytest.mark.parametrize(
         (""stream_name"", ""date_field"", ""expected_date_value""),
         (
-            (""GET_SELLER_FEEDBACK_DATA"", ""date"", ""2020-10-20""),
-            (""GET_LEDGER_DETAIL_VIEW_DATA"", ""Date"", ""2021-11-21""),
-            (""GET_LEDGER_SUMMARY_VIEW_DATA"", ""Date"", ""2022-12-22""),
+            (""GET_SELLER_FEEDBACK_DATA"", ""date"", ""2023-10-20""),
+            (""GET_LEDGER_DETAIL_VIEW_DATA"", ""Date"", ""2023-11-21""),
+            (""GET_LEDGER_SUMMARY_VIEW_DATA"", ""Date"", ""2023-12-22""),
         ),
     )
     @HttpMocker()
     def test_given_report_with_incorrect_date_format_when_read_then_formatted(
         self, stream_name: str, date_field: str, expected_date_value: str, http_mocker: HttpMocker
     ) -> None:
+        http_mocker.clear_all_matchers()
         mock_auth(http_mocker)
 
         http_mocker.post(_create_report_request(stream_name).build(), _create_report_response(_REPORT_ID))
@@ -432,25 +416,27 @@ def test_given_report_with_incorrect_date_format_when_read_then_formatted(
     def test_given_http_error_500_on_create_report_when_read_then_no_records_and_error_logged(
         self, stream_name: str, data_format: str, http_mocker: HttpMocker
     ) -> None:
+        http_mocker.clear_all_matchers()
         mock_auth(http_mocker)
 
         http_mocker.post(
             _create_report_request(stream_name).build(),
             response_with_status(status_code=HTTPStatus.INTERNAL_SERVER_ERROR),
         )
 
-        message_on_backoff_exception = f""The report for stream '{stream_name}' was cancelled due to several failed retry attempts.""
+        message_on_backoff_exception = ""Giving up _send(...) after 6 tries""
 
         output = self._read(stream_name, config())
 
-        assert output.errors[0].trace.error.failure_type == FailureType.system_error
-        assert message_on_backoff_exception in output.errors[0].trace.error.message
+        assert output.errors[0].trace.error.failure_type == FailureType.config_error
+        assert_message_in_log_output(message=message_on_backoff_exception, entrypoint_output=output, log_level=Level.ERROR)
 
     @pytest.mark.parametrize((""stream_name"", ""data_format""), STREAMS)
     @HttpMocker()
     def test_given_http_error_not_support_account_id_of_type_vendor_when_read_then_no_records_and_error_logged(
         self, stream_name: str, data_format: str, http_mocker: HttpMocker
     ):
+        http_mocker.clear_all_matchers()
         mock_auth(http_mocker)
         response_body = {
             ""errors"": [
@@ -467,16 +453,14 @@ def test_given_http_error_not_support_account_id_of_type_vendor_when_read_then_n
         )
 
         warning_message = (
-            ""The endpoint https://sellingpartnerapi-na.amazon.com/reports/2021-06-30/reports returned 400: ""
-            ""Report type 301 does not support account ID of type class com.amazon.partner.account.id.VendorGroupId..""
-            "" This is most likely due to account type (Vendor) on the credentials in use.""
-            "" Try to re-authenticate with Seller account type and sync again.""
+            ""'POST' request to 'https://sellingpartnerapi-na.amazon.com/reports/2021-06-30/reports' failed with status code '400' and""
+            "" error message: 'Report type 301 does not support account ID of type class com.amazon.partner.account.id.VendorGroupId.'.""
         )
 
         output = self._read(stream_name, config())
 
         assert output.errors[0].trace.error.failure_type == FailureType.config_error
-        assert warning_message in output.errors[0].trace.error.message
+        assert_message_in_log_output(message=warning_message, entrypoint_output=output, log_level=Level.ERROR)
 
 
 @freezegun.freeze_time(NOW.isoformat())
@@ -503,6 +487,7 @@ def _read(
     def test_given_report_when_read_then_default_cursor_field_added_to_every_record(
         self, stream_name: str, data_format: str, http_mocker: HttpMocker
     ) -> None:
+        http_mocker.clear_all_matchers()
         mock_auth(http_mocker)
 
         http_mocker.post(_create_report_request(stream_name).build(), _create_report_response(_REPORT_ID))
@@ -527,7 +512,11 @@ def test_given_report_when_read_then_default_cursor_field_added_to_every_record(
     def test_given_report_when_read_then_state_message_produced_and_state_match_latest_record(
         self, stream_name: str, data_format: str, http_mocker: HttpMocker
     ) -> None:
+        """"""
+        This test requires datetime from the records to be higher than the start date of the stream else the cursor value will be the start date
+        """"""
         _config = config()
+        http_mocker.clear_all_matchers()
         mock_auth(http_mocker)
 
         http_mocker.post(_create_report_request(stream_name).build(), _create_report_response(_REPORT_ID))
@@ -545,13 +534,16 @@ def test_given_report_when_read_then_state_message_produced_and_state_match_late
         )
 
         output = self._read(stream_name, _config)
-        assert len(output.state_messages) == 1
+        assert (
+            len(output.state_messages) == 2
+        )  # we have two messages here, one for the slice and once of the ""ensure_at_least_one_state_emitted""
 
         cursor_field = get_stream_by_name(stream_name, _config.build()).cursor_field
         cursor_value_from_latest_record = output.records[-1].record.data.get(cursor_field)
 
         most_recent_state = output.most_recent_state.stream_state
-        assert most_recent_state == {cursor_field: cursor_value_from_latest_record}
+        # format between record and cursor value can differ hence we rely on pendulum parsing to ignore those discrepancies
+        assert pendulum.parse(most_recent_state.__dict__[cursor_field]) == pendulum.parse(cursor_value_from_latest_record)
 
 
 @freezegun.freeze_time(NOW.isoformat())
@@ -585,6 +577,7 @@ def _get_report_request_body(selling_program: str) -> str:
     @pytest.mark.parametrize(""selling_program"", selling_program)
     @HttpMocker()
     def test_given_report_when_read_then_return_records(self, selling_program: str, http_mocker: HttpMocker) -> None:
+        http_mocker.clear_all_matchers()
         mock_auth(http_mocker)
         stream_name = self._get_stream_name(selling_program)
         create_report_request_body = self._get_report_request_body(selling_program)
@@ -600,6 +593,7 @@ def test_given_report_when_read_then_return_records(self, selling_program: str,
             _get_document_download_url_request(_REPORT_DOCUMENT_ID).build(),
             _get_document_download_url_response(_DOCUMENT_DOWNLOAD_URL, _REPORT_DOCUMENT_ID),
         )
+
         http_mocker.get(
             _download_document_request(_DOCUMENT_DOWNLOAD_URL).build(),
             _download_document_response(stream_name, data_format=self.data_format),
@@ -611,6 +605,7 @@ def test_given_report_when_read_then_return_records(self, selling_program: str,
     @pytest.mark.parametrize(""selling_program"", selling_program)
     @HttpMocker()
     def test_given_compressed_report_when_read_then_return_records(self, selling_program: str, http_mocker: HttpMocker) -> None:
+        http_mocker.clear_all_matchers()
         mock_auth(http_mocker)
         stream_name = self._get_stream_name(selling_program)
         create_report_request_body = self._get_report_request_body(selling_program)
@@ -647,6 +642,7 @@ def test_given_compressed_report_when_read_then_return_records(self, selling_pro
     def test_given_http_status_500_then_200_when_create_report_then_retry_and_return_records(
         self, selling_program: str, http_mocker: HttpMocker
     ) -> None:
+        http_mocker.clear_all_matchers()
         mock_auth(http_mocker)
         stream_name = self._get_stream_name(selling_program)
         create_report_request_body = self._get_report_request_body(selling_program)
@@ -675,6 +671,7 @@ def test_given_http_status_500_then_200_when_create_report_then_retry_and_return
     def test_given_http_status_500_then_200_when_retrieve_report_then_retry_and_return_records(
         self, selling_program: str, http_mocker: HttpMocker
     ) -> None:
+        http_mocker.clear_all_matchers()
         mock_auth(http_mocker)
         stream_name = self._get_stream_name(selling_program)
         create_report_request_body = self._get_report_request_body(selling_program)
@@ -706,6 +703,7 @@ def test_given_http_status_500_then_200_when_retrieve_report_then_retry_and_retu
     def test_given_http_status_500_then_200_when_get_document_url_then_retry_and_return_records(
         self, selling_program: str, http_mocker: HttpMocker
     ) -> None:
+        http_mocker.clear_all_matchers()
         mock_auth(http_mocker)
         stream_name = self._get_stream_name(selling_program)
         create_report_request_body = self._get_report_request_body(selling_program)
@@ -737,6 +735,7 @@ def test_given_http_status_500_then_200_when_get_document_url_then_retry_and_ret
     def test_given_http_status_500_then_200_when_download_document_then_retry_and_return_records(
         self, selling_program: str, http_mocker: HttpMocker
     ) -> None:
+        http_mocker.clear_all_matchers()
         mock_auth(http_mocker)
         stream_name = self._get_stream_name(selling_program)
         create_report_request_body = self._get_report_request_body(selling_program)
@@ -768,6 +767,7 @@ def test_given_http_status_500_then_200_when_download_document_then_retry_and_re
     def test_given_report_access_forbidden_when_read_then_no_records_and_error_logged(
         self, selling_program: str, http_mocker: HttpMocker
     ) -> None:
+        http_mocker.clear_all_matchers()
         mock_auth(http_mocker)
         stream_name = self._get_stream_name(selling_program)
         create_report_request_body = self._get_report_request_body(selling_program)
@@ -777,10 +777,7 @@ def test_given_report_access_forbidden_when_read_then_no_records_and_error_logge
         )
 
         output = self._read(stream_name, config())
-        message_on_access_forbidden = (
-            ""This is most likely due to insufficient permissions on the credentials in use. ""
-            ""Try to grant required permissions/scopes or re-authenticate.""
-        )
+        message_on_access_forbidden = ""Forbidden. You don't have permission to access this resource.""
         assert output.errors[0].trace.error.failure_type == FailureType.config_error
         assert message_on_access_forbidden in output.errors[0].trace.error.message
 
@@ -789,6 +786,7 @@ def test_given_report_access_forbidden_when_read_then_no_records_and_error_logge
     def test_given_report_status_cancelled_when_read_then_stream_completed_successfully_and_warn_about_cancellation(
         self, selling_program: str, http_mocker: HttpMocker
     ) -> None:
+        http_mocker.clear_all_matchers()
         mock_auth(http_mocker)
         stream_name = self._get_stream_name(selling_program)
         create_report_request_body = self._get_report_request_body(selling_program)
@@ -801,15 +799,16 @@ def test_given_report_status_cancelled_when_read_then_stream_completed_successfu
             _check_report_status_response(stream_name, processing_status=ReportProcessingStatus.CANCELLED),
         )
 
-        message_on_report_cancelled = f""The report for stream '{stream_name}' was cancelled or there is no data to return.""
+        message_on_report_cancelled = f""Exception while syncing stream {stream_name}""
 
         output = self._read(stream_name, config())
-        assert_message_in_log_output(message_on_report_cancelled, output)
+        assert_message_in_log_output(message=message_on_report_cancelled, entrypoint_output=output, log_level=Level.ERROR)
         assert len(output.records) == 0
 
     @pytest.mark.parametrize(""selling_program"", selling_program)
     @HttpMocker()
     def test_given_report_status_fatal_when_read_then_exception_raised(self, selling_program: str, http_mocker: HttpMocker) -> None:
+        http_mocker.clear_all_matchers()
         mock_auth(http_mocker)
         stream_name = self._get_stream_name(selling_program)
         create_report_request_body = self._get_report_request_body(selling_program)
@@ -824,27 +823,16 @@ def test_given_report_status_fatal_when_read_then_exception_raised(self, selling
             ),
         )
 
-        http_mocker.get(
-            _get_document_download_url_request(_REPORT_DOCUMENT_ID).build(),
-            _get_document_download_url_response(_DOCUMENT_DOWNLOAD_URL, _REPORT_DOCUMENT_ID),
-        )
-        http_mocker.get(
-            _download_document_request(_DOCUMENT_DOWNLOAD_URL).build(),
-            [
-                response_with_status(status_code=HTTPStatus.INTERNAL_SERVER_ERROR),
-                _download_document_error_response(),
-            ],
-        )
-
         output = self._read(stream_name, config(), expecting_exception=True)
         assert output.errors[-1].trace.error.failure_type == FailureType.config_error
-        assert f""Failed to retrieve the report '{stream_name}'"" in output.errors[-1].trace.error.message
+        assert ""At least one job could not be completed for slice {}"" in output.errors[-1].trace.error.message
 
     @pytest.mark.parametrize(""selling_program"", selling_program)
     @HttpMocker()
     def test_given_http_error_500_on_create_report_when_read_then_no_records_and_error_logged(
         self, selling_program: str, http_mocker: HttpMocker
     ) -> None:
+        http_mocker.clear_all_matchers()
         mock_auth(http_mocker)
         stream_name = self._get_stream_name(selling_program)
         create_report_request_body = self._get_report_request_body(selling_program)
@@ -853,9 +841,9 @@ def test_given_http_error_500_on_create_report_when_read_then_no_records_and_err
             response_with_status(status_code=HTTPStatus.INTERNAL_SERVER_ERROR),
         )
 
-        message_on_backoff_exception = f""The report for stream '{stream_name}' was cancelled due to several failed retry attempts.""
+        message_on_backoff_exception = ""Giving up _send(...) after 6 tries""
 
         output = self._read(stream_name, config())
 
-        assert output.errors[0].trace.error.failure_type == FailureType.system_error
-        assert message_on_backoff_exception in output.errors[0].trace.error.message
+        assert output.errors[0].trace.error.failure_type == FailureType.config_error
+        assert_message_in_log_output(message=message_on_backoff_exception, entrypoint_output=output, log_level=Level.ERROR)