@@ -182,20 +182,11 @@ def test_given_state_when_read_then_query_events_using_types_and_state_value_plu
         creation_datetime_of_setup_attempt = int(state_datetime.timestamp()) + 5
 
         http_mocker.get(
-            _events_request()
-            .with_created_gte(state_datetime + _AVOIDING_INCLUSIVE_BOUNDARIES)
-            .with_created_lte(_NOW)
-            .with_limit(100)
-            .with_types(_EVENT_TYPES)
-            .build(),
+            _events_request().with_created_gte(state_datetime).with_created_lte(_NOW).with_limit(100).with_types(_EVENT_TYPES).build(),
             _events_response().with_record(self._a_setup_intent_event(cursor_value, _SETUP_INTENT_ID_1)).build(),
         )
         http_mocker.get(
-            _setup_attempts_request(_SETUP_INTENT_ID_1)
-            .with_created_gte(state_datetime + _AVOIDING_INCLUSIVE_BOUNDARIES)
-            .with_created_lte(_NOW)
-            .with_limit(100)
-            .build(),
+            _setup_attempts_request(_SETUP_INTENT_ID_1).with_created_gte(state_datetime).with_created_lte(_NOW).with_limit(100).build(),
             _setup_attempts_response().with_record(_a_setup_attempt().with_cursor(creation_datetime_of_setup_attempt)).build(),
         )
 
@@ -207,7 +198,7 @@ def test_given_state_when_read_then_query_events_using_types_and_state_value_plu
         assert len(output.records) == 1
         most_recent_state = output.most_recent_state
         assert most_recent_state.stream_descriptor == StreamDescriptor(name=_STREAM_NAME)
-        assert most_recent_state.stream_state == AirbyteStateBlob(created=creation_datetime_of_setup_attempt)
+        assert int(most_recent_state.stream_state.state[""created""]) == int(creation_datetime_of_setup_attempt)
 
     def _a_setup_intent_event(self, cursor_value: int, setup_intent_id: str) -> RecordBuilder:
         return _an_event().with_cursor(cursor_value).with_field(_DATA_FIELD, _a_setup_intent().with_id(setup_intent_id).build())