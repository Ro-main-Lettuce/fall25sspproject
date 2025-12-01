@@ -166,24 +166,22 @@ def test_given_slice_range_when_read_then_perform_multiple_requests(self, http_m
         slice_datetime = start_date + slice_range
 
         http_mocker.get(
-            _application_fees_request().with_created_gte(start_date).with_created_lte(slice_datetime).with_limit(100).build(),
+            _application_fees_request().with_created_gte(slice_datetime).with_created_lte(_NOW).with_limit(100).build(),
             _application_fees_response().build(),
         )
         http_mocker.get(
             _application_fees_request()
-            .with_created_gte(slice_datetime + _AVOIDING_INCLUSIVE_BOUNDARIES)
-            .with_created_lte(_NOW)
+            .with_created_gte(start_date)
+            .with_created_lte(slice_datetime - _AVOIDING_INCLUSIVE_BOUNDARIES)
             .with_limit(100)
             .build(),
             _application_fees_response().build(),
         )
 
         self._read(_config().with_start_date(start_date).with_slice_range_in_days(slice_range.days))
 
-        # request matched http_mocker
-
     @HttpMocker()
-    def test_given_http_status_400_when_read_then_stream_did_not_run(self, http_mocker: HttpMocker) -> None:
+    def test_given_http_status_400_when_read_then_stream_incomplete(self, http_mocker: HttpMocker) -> None:
         http_mocker.get(
             _application_fees_request().with_any_query_params().build(),
             a_response_with_status(400),
@@ -250,21 +248,16 @@ def test_given_no_state_when_read_then_use_application_fees_endpoint(self, http_
         output = self._read(_config().with_start_date(_A_START_DATE), _NO_STATE)
         most_recent_state = output.most_recent_state
         assert most_recent_state.stream_descriptor == StreamDescriptor(name=_STREAM_NAME)
-        assert most_recent_state.stream_state == AirbyteStateBlob(updated=cursor_value)
+        assert most_recent_state.stream_state.updated == str(cursor_value)
 
     @HttpMocker()
     def test_given_state_when_read_then_query_events_using_types_and_state_value_plus_1(self, http_mocker: HttpMocker) -> None:
         start_date = _NOW - timedelta(days=40)
         state_datetime = _NOW - timedelta(days=5)
-        cursor_value = int(state_datetime.timestamp()) + 1
+        cursor_value = int(state_datetime.timestamp())
 
         http_mocker.get(
-            _events_request()
-            .with_created_gte(state_datetime + _AVOIDING_INCLUSIVE_BOUNDARIES)
-            .with_created_lte(_NOW)
-            .with_limit(100)
-            .with_types(_EVENT_TYPES)
-            .build(),
+            _events_request().with_created_gte(state_datetime).with_created_lte(_NOW).with_limit(100).with_types(_EVENT_TYPES).build(),
             _events_response()
             .with_record(_an_event().with_cursor(cursor_value).with_field(_DATA_FIELD, _an_application_fee().build()))
             .build(),
@@ -277,18 +270,13 @@ def test_given_state_when_read_then_query_events_using_types_and_state_value_plu
 
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
             .with_record(_an_event().with_id(""last_record_id_from_first_page"").with_field(_DATA_FIELD, _an_application_fee().build()))
@@ -297,7 +285,7 @@ def test_given_state_and_pagination_when_read_then_return_records(self, http_moc
         http_mocker.get(
             _events_request()
             .with_starting_after(""last_record_id_from_first_page"")
-            .with_created_gte(state_datetime + _AVOIDING_INCLUSIVE_BOUNDARIES)
+            .with_created_gte(state_datetime)
             .with_created_lte(_NOW)
             .with_limit(100)
             .with_types(_EVENT_TYPES)
@@ -316,24 +304,19 @@ def test_given_state_and_pagination_when_read_then_return_records(self, http_moc
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
             _events_response().with_record(self._an_application_fee_event()).build(),
         )
         http_mocker.get(
-            _events_request()
-            .with_created_gte(slice_datetime + _AVOIDING_INCLUSIVE_BOUNDARIES)
-            .with_created_lte(_NOW)
-            .with_limit(100)
-            .with_types(_EVENT_TYPES)
-            .build(),
+            _events_request().with_created_gte(slice_datetime).with_created_lte(_NOW).with_limit(100).with_types(_EVENT_TYPES).build(),
             _events_response().with_record(self._an_application_fee_event()).with_record(self._an_application_fee_event()).build(),
         )
 