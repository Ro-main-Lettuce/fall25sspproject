@@ -52,6 +52,8 @@ def test_ingest_insert_bulk(
         # would compete with Pageserver for bandwidth.
         # neon_env_builder.enable_safekeeper_remote_storage(s3_storage())
 
+    neon_env_builder.pageserver_config_override = ""wait_lsn_timeout='600 s'""
+
     neon_env_builder.disable_scrub_on_exit()  # immediate shutdown may leave stray layers
     env = neon_env_builder.init_start()
 
@@ -92,7 +94,18 @@ def insert_rows(endpoint, table, count, value):
                     worker_rows = rows / CONCURRENCY
                     pool.submit(insert_rows, endpoint, f""table{i}"", worker_rows, value)
 
-        end_lsn = Lsn(endpoint.safe_psql(""select pg_current_wal_lsn()"")[0][0])
+        for attempt in range(5):
+            try:
+                end_lsn = Lsn(endpoint.safe_psql(""select pg_current_wal_lsn()"")[0][0])
+                break
+            except Exception as e:
+                # if we disable backpressure, postgres can become unresponsive for longer than a minute
+                # and new connection attempts time out in postgres after 1 minute
+                # so if this happens we retry new connection
+                log.error(f""Attempt {attempt + 1}/5: Failed to select current wal lsn: {e}"")
+            if attempt == 4:
+                log.error(""Exceeded maximum retry attempts for selecting current wal lsn"")
+                raise
 
         # Wait for pageserver to ingest the WAL.
         client = env.pageserver.http_client()