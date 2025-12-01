@@ -466,8 +466,13 @@ def test_perf_counters(neon_simple_env: NeonEnv):
     #
     # 1.5 is the minimum version to contain these views.
     cur.execute(""CREATE EXTENSION neon VERSION '1.5'"")
+    cur.execute(""set neon.monitor_query_exec_time = on"")
     cur.execute(""SELECT * FROM neon_perf_counters"")
     cur.execute(""SELECT * FROM neon_backend_perf_counters"")
+    cur.execute(
+        ""select value from neon_backend_perf_counters where metric='query_time_seconds_count' and pid=pg_backend_pid()""
+    )
+    assert cur.fetchall()[0][0] == 2
 
 
 def collect_metric(