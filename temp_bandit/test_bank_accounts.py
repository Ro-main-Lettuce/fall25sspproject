@@ -159,7 +159,6 @@ def test_given_source_is_not_bank_account_when_read_then_filter_record(self, htt
             .with_record(_a_customer().with_field(_SOURCES_FIELD, _as_dict(_bank_accounts_response().with_record(_NOT_A_BANK_ACCOUNT))))
             .build(),
         )
-
         output = self._read(_config().with_start_date(_A_START_DATE))
 
         assert len(output.records) == 0
@@ -243,20 +242,15 @@ def test_given_slice_range_when_read_then_perform_multiple_requests(self, http_m
             _customers_request()
             .with_expands(_EXPANDS)
             .with_created_gte(start_date)
-            .with_created_lte(slice_datetime)
+            .with_created_lte(slice_datetime - _AVOIDING_INCLUSIVE_BOUNDARIES)
             .with_limit(100)
             .build(),
             _customers_response()
             .with_record(_a_customer().with_field(_SOURCES_FIELD, _as_dict(_bank_accounts_response().with_record(_a_bank_account()))))
             .build(),
         )
         http_mocker.get(
-            _customers_request()
-            .with_expands(_EXPANDS)
-            .with_created_gte(slice_datetime + _AVOIDING_INCLUSIVE_BOUNDARIES)
-            .with_created_lte(_NOW)
-            .with_limit(100)
-            .build(),
+            _customers_request().with_expands(_EXPANDS).with_created_gte(slice_datetime).with_created_lte(_NOW).with_limit(100).build(),
             _customers_response()
             .with_record(_a_customer().with_field(_SOURCES_FIELD, _as_dict(_bank_accounts_response().with_record(_a_bank_account()))))
             .build(),
@@ -283,7 +277,7 @@ def test_given_slice_range_and_bank_accounts_pagination_when_read_then_do_not_sl
             _customers_request()
             .with_expands(_EXPANDS)
             .with_created_gte(start_date)
-            .with_created_lte(slice_datetime)
+            .with_created_lte(slice_datetime - _AVOIDING_INCLUSIVE_BOUNDARIES)
             .with_limit(100)
             .build(),
             _customers_response()
@@ -297,6 +291,7 @@ def test_given_slice_range_and_bank_accounts_pagination_when_read_then_do_not_sl
             )
             .build(),
         )
+
         http_mocker.get(
             # slice range is not applied here
             _customers_bank_accounts_request(""parent_id"").with_limit(100).with_starting_after(""latest_bank_account_id"").build(),
@@ -386,7 +381,7 @@ def test_given_no_state_and_successful_sync_when_read_then_set_state_to_now(self
 
         most_recent_state = output.most_recent_state
         assert most_recent_state.stream_descriptor == StreamDescriptor(name=_STREAM_NAME)
-        assert most_recent_state.stream_state == AirbyteStateBlob(updated=int(_NOW.timestamp()))
+        assert int(most_recent_state.stream_state.state[""updated""]) == int(_NOW.timestamp())
 
     @HttpMocker()
     def test_given_state_when_read_then_query_events_using_types_and_state_value_plus_1(self, http_mocker: HttpMocker) -> None:
@@ -395,12 +390,7 @@ def test_given_state_when_read_then_query_events_using_types_and_state_value_plu
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
             .with_record(_an_event().with_cursor(cursor_value).with_field(_DATA_FIELD, _a_bank_account().build()))
             .build(),
@@ -413,18 +403,13 @@ def test_given_state_when_read_then_query_events_using_types_and_state_value_plu
 
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
             .with_record(_an_event().with_id(""last_record_id_from_first_page"").with_field(_DATA_FIELD, _a_bank_account().build()))
@@ -433,7 +418,7 @@ def test_given_state_and_pagination_when_read_then_return_records(self, http_moc
         http_mocker.get(
             _events_request()
             .with_starting_after(""last_record_id_from_first_page"")
-            .with_created_gte(state_datetime + _AVOIDING_INCLUSIVE_BOUNDARIES)
+            .with_created_gte(state_datetime)
             .with_created_lte(_NOW)
             .with_limit(100)
             .with_types(_EVENT_TYPES)
@@ -452,24 +437,19 @@ def test_given_state_and_pagination_when_read_then_return_records(self, http_moc
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
             _events_response().with_record(self._a_bank_account_event()).build(),
         )
         http_mocker.get(
-            _events_request()
-            .with_created_gte(slice_datetime + _AVOIDING_INCLUSIVE_BOUNDARIES)
-            .with_created_lte(_NOW)
-            .with_limit(100)
-            .with_types(_EVENT_TYPES)
-            .build(),
+            _events_request().with_created_gte(slice_datetime).with_created_lte(_NOW).with_limit(100).with_types(_EVENT_TYPES).build(),
             _events_response().with_record(self._a_bank_account_event()).with_record(self._a_bank_account_event()).build(),
         )
 
@@ -510,12 +490,7 @@ def test_given_state_earlier_than_30_days_when_read_then_query_events_using_type
     def test_given_source_is_not_bank_account_when_read_then_filter_record(self, http_mocker: HttpMocker) -> None:
         state_datetime = _NOW - timedelta(days=5)
         http_mocker.get(
-            _events_request()
-            .with_created_gte(state_datetime + _AVOIDING_INCLUSIVE_BOUNDARIES)
-            .with_created_lte(_NOW)
-            .with_limit(100)
-            .with_types(_EVENT_TYPES)
-            .build(),
+            _events_request().with_created_gte(state_datetime).with_created_lte(_NOW).with_limit(100).with_types(_EVENT_TYPES).build(),
             _events_response().with_record(_an_event().with_field(_DATA_FIELD, _NOT_A_BANK_ACCOUNT.build())).build(),
         )
 