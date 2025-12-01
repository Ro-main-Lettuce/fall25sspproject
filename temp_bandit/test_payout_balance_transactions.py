@@ -167,12 +167,7 @@ def test_when_read_then_fetch_from_updated_payouts(self, http_mocker: HttpMocker
         state = StateBuilder().with_stream_state(_STREAM_NAME, {""updated"": int(_STATE_DATE.timestamp())}).build()
         catalog = _create_catalog(SyncMode.incremental)
         http_mocker.get(
-            _events_request()
-            .with_created_gte(_STATE_DATE + _AVOIDING_INCLUSIVE_BOUNDARIES)
-            .with_created_lte(_NOW)
-            .with_limit(100)
-            .with_types(_EVENT_TYPES)
-            .build(),
+            _events_request().with_created_gte(_STATE_DATE).with_created_lte(_NOW).with_limit(100).with_types(_EVENT_TYPES).build(),
             _events_response()
             .with_record(_event_record().with_field(_DATA_FIELD, _create_payout_record().with_id(_A_PAYOUT_ID).build()))
             .build(),