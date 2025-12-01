@@ -74,8 +74,9 @@ def test_hot_standby(neon_simple_env: NeonEnv):
                 for query in queries:
                     with s_con.cursor() as secondary_cursor:
                         secondary_cursor.execute(query)
-                        response = secondary_cursor.fetchone()
-                        assert response is not None
+                        res = secondary_cursor.fetchone()
+                        assert res is not None
+                        response = res
                         assert response == responses[query]
 
             # Check for corrupted WAL messages which might otherwise go unnoticed if
@@ -164,7 +165,7 @@ def test_hot_standby_gc(neon_env_builder: NeonEnvBuilder, pause_apply: bool):
 
             s_cur.execute(""SELECT COUNT(*) FROM test"")
             res = s_cur.fetchone()
-            assert res[0] == 10000
+            assert res == (10000,)
 
             # Clear the cache in the standby, so that when we
             # re-execute the query, it will make GetPage
@@ -195,7 +196,7 @@ def test_hot_standby_gc(neon_env_builder: NeonEnvBuilder, pause_apply: bool):
             s_cur.execute(""SELECT COUNT(*) FROM test"")
             log_replica_lag(primary, secondary)
             res = s_cur.fetchone()
-            assert res[0] == 10000
+            assert res == (10000,)
 
 
 def run_pgbench(connstr: str, pg_bin: PgBin):