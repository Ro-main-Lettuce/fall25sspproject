@@ -239,6 +239,8 @@ def test_isolation(
             ""neon.regress_test_mode = true"",
             # Stack size should be increased for tests to pass with asan.
             ""max_stack_depth = 4MB"",
+            # Neon extensiosn starts 2 BGW so decreasing number of parallel workers which can affect deadlock-parallel test if it hits max_worker_processes.
+            ""max_worker_processes = 16"",
         ],
     )
     endpoint.safe_psql(f""CREATE DATABASE {DBNAME}"")