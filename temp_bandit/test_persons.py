@@ -332,7 +332,7 @@ def test_incremental_with_newer_start_date(self, http_mocker):
             _create_response().with_record(record=_create_persons_event_record(event_type=""person.created"")).build(),
         )
 
-        state = StateBuilder().with_stream_state(_STREAM_NAME, {""updated"": int(state_datetime.timestamp())}).build()
+        state = StateBuilder().with_stream_state(_STREAM_NAME, {""updated"": str(state_datetime.timestamp())}).build()
         source = SourceStripe(config=config, catalog=_create_catalog(sync_mode=SyncMode.incremental), state=state)
         actual_messages = read(
             source,