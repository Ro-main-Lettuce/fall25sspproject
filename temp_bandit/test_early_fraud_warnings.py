@@ -1,4 +1,3 @@
-#
 # Copyright (c) 2025 Airbyte, Inc., all rights reserved.
 #
 
@@ -209,7 +208,7 @@ def test_given_no_state_when_read_then_use_early_fraud_warnings_endpoint(self, h
         output = self._read(_config().with_start_date(_A_START_DATE), _NO_STATE)
         most_recent_state = output.most_recent_state
         assert most_recent_state.stream_descriptor == StreamDescriptor(name=_STREAM_NAME)
-        assert most_recent_state.stream_state == AirbyteStateBlob(updated=cursor_value)
+        assert most_recent_state.stream_state.updated == str(cursor_value)
 
     @HttpMocker()
     def test_given_state_when_read_then_query_events_using_types_and_state_value_plus_1(self, http_mocker: HttpMocker) -> None:
@@ -218,12 +217,7 @@ def test_given_state_when_read_then_query_events_using_types_and_state_value_plu
         cursor_value = int(state_datetime.timestamp()) + 1
 
         http_mocker.get(
-            _events_request()
-            .with_created_gte(state_datetime + _AVOIDING_INCLUSIVE_BOUNDARIES)
-            .with_created_lte(_NOW)
-            .with_limit(100)
-            .with_types(_EVENT_TYPES)
-            .build(),
+            _events_request().with_created_gte(state_datetime).with_created_lte(_NOW).with_limit(100).with_types(_EVENT_TYPES).build(),
             _events_response()
             .with_record(_an_event().with_cursor(cursor_value).with_field(_DATA_FIELD, _an_early_fraud_warning().build()))
             .build(),
@@ -236,18 +230,13 @@ def test_given_state_when_read_then_query_events_using_types_and_state_value_plu
 
         most_recent_state = output.most_recent_state
         assert most_recent_state.stream_descriptor == StreamDescriptor(name=_STREAM_NAME)
-        assert most_recent_state.stream_state == AirbyteStateBlob(updated=cursor_value)
+        assert most_recent_state.stream_state.updated == str(cursor_value)
 
     @HttpMocker()
     def test_given_state_and_pagination_when_read_then_return_records(self, http_mocker: HttpMocker) -> None:
         state_datetime = _NOW - timedelta(days=5)
         http_mocker.get(
-            _events_request()
-            .with_created_gte(state_datetime + _AVOIDING_INCLUSIVE_BOUNDARIES)
-            .with_created_lte(_NOW)
-            .with_limit(100)
-            .with_types(_EVENT_TYPES)
-            .build(),
+            _events_request().with_created_gte(state_datetime).with_created_lte(_NOW).with_limit(100).with_types(_EVENT_TYPES).build(),
             _events_response()
             .with_pagination()
             .with_record(_an_event().with_id(""last_record_id_from_first_page"").with_field(_DATA_FIELD, _an_early_fraud_warning().build()))
@@ -256,7 +245,7 @@ def test_given_state_and_pagination_when_read_then_return_records(self, http_moc
         http_mocker.get(
             _events_request()
             .with_starting_after(""last_record_id_from_first_page"")
-            .with_created_gte(state_datetime + _AVOIDING_INCLUSIVE_BOUNDARIES)
+            .with_created_gte(state_datetime)
             .with_created_lte(_NOW)
             .with_limit(100)
             .with_types(_EVENT_TYPES)
@@ -275,24 +264,19 @@ def test_given_state_and_pagination_when_read_then_return_records(self, http_moc
     def test_given_state_and_small_slice_range_when_read_then_perform_multiple_queries(self, http_mocker: HttpMocker) -> None:
         state_datetime = _NOW - timedelta(days=5)
         slice_range = timedelta(days=3)
-        slice_datetime = state_datetime + _AVOIDING_INCLUSIVE_BOUNDARIES + slice_range
+        slice_datetime = state_datetime + slice_range
 
         http_mocker.get(
             _events_request()
-            .with_created_gte(state_datetime + _AVOIDING_INCLUSIVE_BOUNDARIES)
-            .with_created_lte(slice_datetime)
+            .with_created_gte(state_datetime)
+            .with_created_lte(slice_datetime - _AVOIDING_INCLUSIVE_BOUNDARIES)
             .with_limit(100)
             .with_types(_EVENT_TYPES)
             .build(),
             _events_response().with_record(self._an_early_fraud_warning_event()).build(),
         )
         http_mocker.get(
-            _events_request()
-            .with_created_gte(slice_datetime + _AVOIDING_INCLUSIVE_BOUNDARIES)
-            .with_created_lte(_NOW)
-            .with_limit(100)
-            .with_types(_EVENT_TYPES)
-            .build(),
+            _events_request().with_created_gte(slice_datetime).with_created_lte(_NOW).with_limit(100).with_types(_EVENT_TYPES).build(),
             _events_response().with_record(self._an_early_fraud_warning_event()).with_record(self._an_early_fraud_warning_event()).build(),
         )
 