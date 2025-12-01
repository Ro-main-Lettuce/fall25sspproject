@@ -15,11 +15,10 @@ def configure_catalog():
         stream[""json_schema""] = {}
     streams = [
         ConfiguredAirbyteStream(
-            stream=stream.get(""name""),
-            sync_mode=stream.get(""supported_sync_modes"", [])[0],
-            destination_sync_mode=DestinationSyncMode.append
+            stream=stream.get(""name""), sync_mode=stream.get(""supported_sync_modes"", [])[0], destination_sync_mode=DestinationSyncMode.append
         )
-        for stream in catalog_streams if stream.get(""supported_sync_modes"")
+        for stream in catalog_streams
+        if stream.get(""supported_sync_modes"")
     ]
     configured_catalog = ConfiguredAirbyteCatalog(streams=streams)
 
@@ -35,10 +34,10 @@ def configure_catalog():
                 ""stream"": {
                     ""name"": stream.stream.name if hasattr(stream.stream, ""name"") else stream.stream,
                     ""supported_sync_modes"": [""full_refresh""],
-                    ""json_schema"": {}
+                    ""json_schema"": {},
                 },
                 ""sync_mode"": str(stream.sync_mode),
-                ""destination_sync_mode"": ""append""
+                ""destination_sync_mode"": ""append"",
             }
             result[""streams""].append(stream_dict)
         json.dump(result, outfile, indent=2, sort_keys=True)