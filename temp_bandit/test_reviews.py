@@ -265,7 +265,7 @@ def test_given_state_when_read_then_query_events_using_types_and_state_value_plu
 
         output = self._read(
             _config().with_start_date(start_date),
-            StateBuilder().with_stream_state(_STREAM_NAME, {""updated"": int(state_datetime.timestamp())}).build(),
+            StateBuilder().with_stream_state(_STREAM_NAME, {""updated"": str(state_datetime.timestamp())}).build(),
         )
 
         most_recent_state = output.most_recent_state