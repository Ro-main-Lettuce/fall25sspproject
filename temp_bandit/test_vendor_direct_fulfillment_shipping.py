@@ -9,6 +9,7 @@
 import freezegun
 import pendulum
 
+from airbyte_cdk.models import AirbyteStateMessage, FailureType, SyncMode
 from airbyte_cdk.test.entrypoint_wrapper import EntrypointOutput
 from airbyte_cdk.test.mock_http import HttpMocker
 from airbyte_cdk.test.mock_http.response_builder import (
@@ -21,7 +22,6 @@
     find_template,
 )
 from airbyte_cdk.test.state_builder import StateBuilder
-from airbyte_protocol.models import AirbyteStateMessage, FailureType, SyncMode
 
 from .config import NOW, TIME_FORMAT, ConfigBuilder
 from .pagination import NEXT_TOKEN_STRING, VendorFulfillmentPaginationStrategy
@@ -115,15 +115,15 @@ def test_given_two_slices_when_read_then_return_records(self, http_mocker: HttpM
 
         query_params_first_slice = {
             _REPLICATION_START_FIELD: _START_DATE.strftime(TIME_FORMAT),
-            _REPLICATION_END_FIELD: _START_DATE.add(days=7).strftime(TIME_FORMAT),
+            _REPLICATION_END_FIELD: _START_DATE.add(days=6, hours=23, minutes=59, seconds=59).strftime(TIME_FORMAT),
         }
         http_mocker.get(
             _vendor_direct_fulfillment_shipping_request().with_query_params(query_params_first_slice).build(),
             _vendor_direct_fulfillment_shipping_response().with_record(_shipping_label_record()).build(),
         )
 
         query_params_second_slice = {
-            _REPLICATION_START_FIELD: query_params_first_slice[_REPLICATION_END_FIELD],
+            _REPLICATION_START_FIELD: _START_DATE.add(days=7).strftime(TIME_FORMAT),
             _REPLICATION_END_FIELD: end_date.strftime(TIME_FORMAT),
         }
         http_mocker.get(
@@ -198,31 +198,20 @@ def test_when_read_then_state_message_produced_and_state_match_latest_record(sel
         )
 
         output = self._read(config().with_start_date(_START_DATE).with_end_date(_END_DATE))
-        assert len(output.state_messages) == 1
+        assert len(output.state_messages) == 2
 
         cursor_value_from_latest_record = output.records[-1].record.data.get(_CURSOR_FIELD)
 
         most_recent_state = output.most_recent_state.stream_state
-        assert most_recent_state == {_CURSOR_FIELD: cursor_value_from_latest_record}
+        assert most_recent_state.__dict__ == {_CURSOR_FIELD: cursor_value_from_latest_record}
 
     @HttpMocker()
     def test_given_state_when_read_then_state_value_is_created_after_query_param(self, http_mocker: HttpMocker) -> None:
         mock_auth(http_mocker)
         state_value = _START_DATE.add(days=1).strftime(TIME_FORMAT)
 
-        query_params_first_read = {
-            _REPLICATION_START_FIELD: _START_DATE.strftime(TIME_FORMAT),
-            _REPLICATION_END_FIELD: _END_DATE.strftime(TIME_FORMAT),
-        }
         query_params_incremental_read = {_REPLICATION_START_FIELD: state_value, _REPLICATION_END_FIELD: _END_DATE.strftime(TIME_FORMAT)}
 
-        http_mocker.get(
-            _vendor_direct_fulfillment_shipping_request().with_query_params(query_params_first_read).build(),
-            _vendor_direct_fulfillment_shipping_response()
-            .with_record(_shipping_label_record())
-            .with_record(_shipping_label_record())
-            .build(),
-        )
         http_mocker.get(
             _vendor_direct_fulfillment_shipping_request().with_query_params(query_params_incremental_read).build(),
             _vendor_direct_fulfillment_shipping_response()
@@ -235,4 +224,4 @@ def test_given_state_when_read_then_state_value_is_created_after_query_param(sel
             config_=config().with_start_date(_START_DATE).with_end_date(_END_DATE),
             state=StateBuilder().with_stream_state(_STREAM_NAME, {_CURSOR_FIELD: state_value}).build(),
         )
-        assert output.most_recent_state.stream_state == {_CURSOR_FIELD: _END_DATE.strftime(TIME_FORMAT)}
+        assert output.most_recent_state.stream_state.__dict__ == {_CURSOR_FIELD: _END_DATE.strftime(TIME_FORMAT)}