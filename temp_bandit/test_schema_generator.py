@@ -27,14 +27,22 @@
 def test_configure_catalog():
     stream = AirbyteStream(name=""stream"", supported_sync_modes=[SyncMode.full_refresh], json_schema={})
     catalog = AirbyteCatalog(streams=[stream])
-    catalog_message = AirbyteMessage(type=Type.CATALOG, catalog=catalog)
-    sys.stdin = io.StringIO(catalog_message.json())
+    catalog_dict = {""type"": ""CATALOG"", ""catalog"": {""streams"": [{""name"": ""stream"", ""supported_sync_modes"": [""full_refresh""], ""json_schema"": {}}]}}
+    sys.stdin = io.StringIO(json.dumps(catalog_dict))
 
-    expected_configured_catalog = ConfiguredAirbyteCatalog(
-        streams=[ConfiguredAirbyteStream(stream=stream, sync_mode=SyncMode.full_refresh, destination_sync_mode=DestinationSyncMode.append)]
-    )
-
-    expected_configured_catalog_json = json.loads(expected_configured_catalog.json())
+    expected_configured_catalog_json = {
+        ""streams"": [
+            {
+                ""stream"": {
+                    ""name"": ""stream"",
+                    ""supported_sync_modes"": [""full_refresh""],
+                    ""json_schema"": {}
+                },
+                ""sync_mode"": ""full_refresh"",
+                ""destination_sync_mode"": ""append""
+            }
+        ]
+    }
 
     with tempfile.TemporaryDirectory() as temp_dir:
         os.chdir(temp_dir)
@@ -48,15 +56,16 @@ def test_configure_catalog():
 
 def test_infer_schemas():
     expected_schema = {
-        ""$schema"": ""http://json-schema.org/schema#"",
+        ""$schema"": ""http://json-schema.org/draft-07/schema#"",
         ""properties"": {""a"": {""type"": ""integer""}, ""b"": {""type"": ""string""}},
         ""type"": ""object"",
+        ""additionalProperties"": True,
     }
 
     with tempfile.TemporaryDirectory() as temp_dir:
         os.chdir(temp_dir)
         record = {""a"": 1, ""b"": ""test""}
-        record_message = AirbyteMessage(type=Type.RECORD, record=AirbyteRecordMessage(stream=""stream"", data=record, emitted_at=111)).json()
+        record_message = json.dumps({""type"": ""RECORD"", ""record"": {""stream"": ""stream"", ""data"": record, ""emitted_at"": 111}})
         sys.stdin = io.StringIO(record_message)
         infer_schemas()
         assert os.path.exists(""schemas/stream.json"")