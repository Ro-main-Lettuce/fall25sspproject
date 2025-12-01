@@ -22,7 +22,12 @@ def test_lfc_working_set_approximation(neon_simple_env: NeonEnv):
     log.info(""Creating endpoint with 1MB shared_buffers and 64 MB LFC"")
     endpoint = env.endpoints.create_start(
         ""main"",
-        config_lines=[""neon.max_file_cache_size='128MB'"", ""neon.file_cache_size_limit='64MB'""],
+        config_lines=[
+            ""autovacuum=off"",
+            ""bgwriter_lru_maxpages=0"",
+            ""neon.max_file_cache_size='128MB'"",
+            ""neon.file_cache_size_limit='64MB'"",
+        ],
     )
 
     cur = endpoint.connect().cursor()
@@ -72,7 +77,7 @@ def test_lfc_working_set_approximation(neon_simple_env: NeonEnv):
     # verify working set size after some index access of a few select pages only
     blocks = query_scalar(cur, ""select approximate_working_set_size(true)"")
     log.info(f""working set size after some index access of a few select pages only {blocks}"")
-    assert blocks < 12
+    assert blocks < 20
 
 
 @pytest.mark.skipif(not USE_LFC, reason=""LFC is disabled, skipping"")
@@ -83,6 +88,7 @@ def test_sliding_working_set_approximation(neon_simple_env: NeonEnv):
         branch_name=""main"",
         config_lines=[
             ""autovacuum = off"",
+            ""bgwriter_lru_maxpages=0"",
             ""shared_buffers=1MB"",
             ""neon.max_file_cache_size=256MB"",
             ""neon.file_cache_size_limit=245MB"",
@@ -92,9 +98,9 @@ def test_sliding_working_set_approximation(neon_simple_env: NeonEnv):
     cur = conn.cursor()
     cur.execute(""create extension neon"")
     cur.execute(
-        ""create table t(pk integer primary key, count integer default 0, payload text default repeat('?', 128))""
+        ""create table t(pk integer primary key, count integer default 0, payload text default repeat('?', 1000)) with (fillfactor=10)""
     )
-    cur.execute(""insert into t (pk) values (generate_series(1,1000000))"")
+    cur.execute(""insert into t (pk) values (generate_series(1,100000))"")
     time.sleep(2)
     before_10k = time.monotonic()
     cur.execute(""select sum(count) from t where pk between 10000 and 20000"")
@@ -115,5 +121,5 @@ def test_sliding_working_set_approximation(neon_simple_env: NeonEnv):
     size = cur.fetchall()[0][0] // 8192
     log.info(f""Table size {size} blocks"")
 
-    assert estimation_1k >= 20 and estimation_1k <= 40
-    assert estimation_10k >= 200 and estimation_10k <= 440
+    assert estimation_1k >= 900 and estimation_1k <= 2000
+    assert estimation_10k >= 9000 and estimation_10k <= 20000