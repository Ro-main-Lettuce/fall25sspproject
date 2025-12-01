@@ -128,8 +128,7 @@ def test_get_schema_root_properties(mocker, monday_requester):
 
 
 def test_build_activity_query(mocker, monday_requester):
-    mock_stream_state = {""updated_at_int"": 1636738688}
-    object_arguments = {""stream_state"": mock_stream_state}
+    object_arguments = {""stream_slice"": {""start_time"": 1636738688}}
     mocker.patch.object(MondayGraphqlRequester, ""_get_object_arguments"", return_value=""stream_state:{{ stream_state['updated_at_int'] }}"")
     requester = monday_requester
 