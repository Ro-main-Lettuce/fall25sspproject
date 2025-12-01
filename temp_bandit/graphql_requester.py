@@ -7,6 +7,7 @@
 from functools import partial
 from typing import Any, Mapping, MutableMapping, Optional, Type, Union
 
+from airbyte_cdk.models import SyncMode
 from airbyte_cdk.sources.declarative.interpolation import InterpolatedString
 from airbyte_cdk.sources.declarative.requesters.http_requester import HttpRequester
 from airbyte_cdk.sources.declarative.schema.json_file_schema_loader import JsonFileSchemaLoader
@@ -26,6 +27,9 @@ def __post_init__(self, parameters: Mapping[str, Any]):
         self.limit = InterpolatedString.create(self.limit, parameters=parameters)
         self.nested_limit = InterpolatedString.create(self.nested_limit, parameters=parameters)
         self.name = parameters.get(""name"", """").lower()
+        self.stream_sync_mode = (
+            SyncMode.full_refresh if parameters.get(""stream_sync_mode"", ""full_refresh"") == ""full_refresh"" else SyncMode.incremental
+        )
 
     def _ensure_type(self, t: Type, o: Any):
         """"""
@@ -159,11 +163,15 @@ def _build_activity_query(self, object_name: str, field_schema: dict, sub_page:
         """"""
         nested_limit = self.nested_limit.eval(self.config)
 
-        created_at = (object_arguments.get(""stream_state"", dict()) or dict()).get(""created_at_int"")
-        object_arguments.pop(""stream_state"")
+        created_at = (object_arguments.get(""stream_slice"", dict()) or dict()).get(""start_time"")
+        if ""stream_slice"" in object_arguments:
+            object_arguments.pop(""stream_slice"")
 
-        if created_at:
-            created_at = datetime.fromtimestamp(created_at).strftime(""%Y-%m-%dT%H:%M:%SZ"")
+        # 1 is default start time, so we can skip it to get all the data
+        if created_at == ""1"":
+            created_at = None
+        else:
+            created_at = datetime.fromtimestamp(int(created_at)).strftime(""%Y-%m-%dT%H:%M:%SZ"")
 
         query = self._build_query(object_name, field_schema, limit=nested_limit, page=sub_page, fromt=created_at)
         if ""board_ids"" in self.config and ""ids"" not in object_arguments:
@@ -197,19 +205,24 @@ def get_request_params(
 
         page = next_page_token and next_page_token[self.NEXT_PAGE_TOKEN_FIELD_NAME]
         if self.name == ""boards"" and stream_slice:
+            if self.stream_sync_mode == SyncMode.full_refresh:
+                # incremental sync parameters are not needed for full refresh
+                stream_slice = {}
+            else:
+                stream_slice = {""ids"": stream_slice.get(""ids"")}
             query_builder = partial(self._build_query, **stream_slice)
         elif self.name == ""items"":
             # `items` stream use a separate pagination strategy where first level pages are across `boards` and sub-pages are across `items`
             page, sub_page = page if page else (None, None)
-            if not stream_slice:
+            if self.stream_sync_mode == SyncMode.full_refresh:
                 query_builder = partial(self._build_items_query, sub_page=sub_page)
             else:
                 query_builder = partial(self._build_items_incremental_query, stream_slice=stream_slice)
         elif self.name == ""teams"":
             query_builder = self._build_teams_query
         elif self.name == ""activity_logs"":
             page, sub_page = page if page else (None, None)
-            query_builder = partial(self._build_activity_query, sub_page=sub_page, stream_state=stream_state)
+            query_builder = partial(self._build_activity_query, sub_page=sub_page, stream_slice=stream_slice)
         else:
             query_builder = self._build_query
         query = query_builder(