@@ -62,7 +62,7 @@
     Records Synced: {sync_result.records_synced}
     Bytes Synced: {sync_result.bytes_synced}
     Job Status: {sync_result.get_job_status()}
-    List of Stream Names: {', '.join(sync_result.stream_names)}
+    List of Stream Names: {"", "".join(sync_result.stream_names)}
     '''
 )
 ```