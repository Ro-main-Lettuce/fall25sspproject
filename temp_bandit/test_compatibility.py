@@ -36,10 +36,8 @@
 # - `test_create_snapshot` a script wrapped in a test that creates a data snapshot.
 # - `test_backward_compatibility` checks that the current version of Neon can start/read/interract with a data snapshot created by the previous version.
 #   The path to the snapshot is configured by COMPATIBILITY_SNAPSHOT_DIR environment variable.
-#   If the breakage is intentional, the test can be xfaild with setting ALLOW_BACKWARD_COMPATIBILITY_BREAKAGE=true.
 # - `test_forward_compatibility` checks that a snapshot created by the current version can be started/read/interracted by the previous version of Neon.
 #   Paths to Neon and Postgres are configured by COMPATIBILITY_NEON_BIN and COMPATIBILITY_POSTGRES_DISTRIB_DIR environment variables.
-#   If the breakage is intentional, the test can be xfaild with setting ALLOW_FORWARD_COMPATIBILITY_BREAKAGE=true.
 #
 # The file contains a couple of helper functions:
 # - check_neon_works performs the test itself, feel free to add more checks there.
@@ -48,7 +46,7 @@
 #
 # How to run `test_backward_compatibility` locally:
 #
-#    export DEFAULT_PG_VERSION=16
+#    export DEFAULT_PG_VERSION=17
 #    export BUILD_TYPE=release
 #    export CHECK_ONDISK_DATA_COMPATIBILITY=true
 #    export COMPATIBILITY_SNAPSHOT_DIR=test_output/compatibility_snapshot_pgv${DEFAULT_PG_VERSION}
@@ -70,7 +68,7 @@
 #
 # How to run `test_forward_compatibility` locally:
 #
-#    export DEFAULT_PG_VERSION=16
+#    export DEFAULT_PG_VERSION=17
 #    export BUILD_TYPE=release
 #    export CHECK_ONDISK_DATA_COMPATIBILITY=true
 #    export COMPATIBILITY_NEON_BIN=neon_previous/target/${BUILD_TYPE}
@@ -96,7 +94,7 @@
 #
 # How to run `test_version_mismatch` locally:
 #
-#    export DEFAULT_PG_VERSION=16
+#    export DEFAULT_PG_VERSION=17
 #    export BUILD_TYPE=release
 #    export CHECK_ONDISK_DATA_COMPATIBILITY=true
 #    export COMPATIBILITY_NEON_BIN=neon_previous/target/${BUILD_TYPE}
@@ -208,37 +206,20 @@ def test_backward_compatibility(
     """"""
     Test that the new binaries can read old data
     """"""
-    breaking_changes_allowed = (
-        os.environ.get(""ALLOW_BACKWARD_COMPATIBILITY_BREAKAGE"", ""false"").lower() == ""true""
-    )
-
-    try:
-        neon_env_builder.num_safekeepers = 3
-        env = neon_env_builder.from_repo_dir(compatibility_snapshot_dir / ""repo"")
-        env.pageserver.allowed_errors.append(ingest_lag_log_line)
-        env.start()
-
-        check_neon_works(
-            env,
-            test_output_dir=test_output_dir,
-            sql_dump_path=compatibility_snapshot_dir / ""dump.sql"",
-            repo_dir=env.repo_dir,
-        )
-
-        env.pageserver.assert_log_contains(ingest_lag_log_line)
-
-    except Exception:
-        if breaking_changes_allowed:
-            pytest.xfail(
-                ""Breaking changes are allowed by ALLOW_BACKWARD_COMPATIBILITY_BREAKAGE env var""
-            )
-        else:
-            raise
+    neon_env_builder.num_safekeepers = 3
+    env = neon_env_builder.from_repo_dir(compatibility_snapshot_dir / ""repo"")
+    env.pageserver.allowed_errors.append(ingest_lag_log_line)
+    env.start()
 
-    assert not breaking_changes_allowed, (
-        ""Breaking changes are allowed by ALLOW_BACKWARD_COMPATIBILITY_BREAKAGE, but the test has passed without any breakage""
+    check_neon_works(
+        env,
+        test_output_dir=test_output_dir,
+        sql_dump_path=compatibility_snapshot_dir / ""dump.sql"",
+        repo_dir=env.repo_dir,
     )
 
+    env.pageserver.assert_log_contains(ingest_lag_log_line)
+
 
 @check_ondisk_data_compatibility_if_enabled
 @pytest.mark.xdist_group(""compatibility"")
@@ -254,72 +235,56 @@ def test_forward_compatibility(
     """"""
     Test that the old binaries can read new data
     """"""
-    breaking_changes_allowed = (
-        os.environ.get(""ALLOW_FORWARD_COMPATIBILITY_BREAKAGE"", ""false"").lower() == ""true""
-    )
 
     neon_env_builder.control_plane_hooks_api = compute_reconfigure_listener.control_plane_hooks_api
     neon_env_builder.test_may_use_compatibility_snapshot_binaries = True
 
-    try:
-        neon_env_builder.num_safekeepers = 3
+    neon_env_builder.num_safekeepers = 3
 
-        # Use previous version's production binaries (pageserver, safekeeper, pg_distrib_dir, etc.).
-        # But always use the current version's neon_local binary.
-        # This is because we want to test the compatibility of the data format, not the compatibility of the neon_local CLI.
-        assert neon_env_builder.compatibility_neon_binpath is not None, (
-            ""the environment variable COMPATIBILITY_NEON_BIN is required""
-        )
-        assert neon_env_builder.compatibility_pg_distrib_dir is not None, (
-            ""the environment variable COMPATIBILITY_POSTGRES_DISTRIB_DIR is required""
-        )
-        neon_env_builder.neon_binpath = neon_env_builder.compatibility_neon_binpath
-        neon_env_builder.pg_distrib_dir = neon_env_builder.compatibility_pg_distrib_dir
+    # Use previous version's production binaries (pageserver, safekeeper, pg_distrib_dir, etc.).
+    # But always use the current version's neon_local binary.
+    # This is because we want to test the compatibility of the data format, not the compatibility of the neon_local CLI.
+    assert neon_env_builder.compatibility_neon_binpath is not None, (
+        ""the environment variable COMPATIBILITY_NEON_BIN is required""
+    )
+    assert neon_env_builder.compatibility_pg_distrib_dir is not None, (
+        ""the environment variable COMPATIBILITY_POSTGRES_DISTRIB_DIR is required""
+    )
+    neon_env_builder.neon_binpath = neon_env_builder.compatibility_neon_binpath
+    neon_env_builder.pg_distrib_dir = neon_env_builder.compatibility_pg_distrib_dir
 
-        env = neon_env_builder.from_repo_dir(
-            compatibility_snapshot_dir / ""repo"",
-        )
-        # there may be an arbitrary number of unrelated tests run between create_snapshot and here
-        env.pageserver.allowed_errors.append(ingest_lag_log_line)
-
-        # not using env.pageserver.version because it was initialized before
-        prev_pageserver_version_str = env.get_binary_version(""pageserver"")
-        prev_pageserver_version_match = re.search(
-            ""Neon page server git(?:-env)?:(.*) failpoints: (.*), features: (.*)"",
-            prev_pageserver_version_str,
+    env = neon_env_builder.from_repo_dir(
+        compatibility_snapshot_dir / ""repo"",
+    )
+    # there may be an arbitrary number of unrelated tests run between create_snapshot and here
+    env.pageserver.allowed_errors.append(ingest_lag_log_line)
+
+    # not using env.pageserver.version because it was initialized before
+    prev_pageserver_version_str = env.get_binary_version(""pageserver"")
+    prev_pageserver_version_match = re.search(
+        ""Neon page server git(?:-env)?:(.*) failpoints: (.*), features: (.*)"",
+        prev_pageserver_version_str,
+    )
+    if prev_pageserver_version_match is not None:
+        prev_pageserver_version = prev_pageserver_version_match.group(1)
+    else:
+        raise AssertionError(
+            ""cannot find git hash in the version string: "" + prev_pageserver_version_str
         )
-        if prev_pageserver_version_match is not None:
-            prev_pageserver_version = prev_pageserver_version_match.group(1)
-        else:
-            raise AssertionError(
-                ""cannot find git hash in the version string: "" + prev_pageserver_version_str
-            )
-
-        # does not include logs from previous runs
-        assert not env.pageserver.log_contains(f""git(-env)?:{prev_pageserver_version}"")
 
-        env.start()
+    # does not include logs from previous runs
+    assert not env.pageserver.log_contains(f""git(-env)?:{prev_pageserver_version}"")
 
-        # ensure the specified pageserver is running
-        assert env.pageserver.log_contains(f""git(-env)?:{prev_pageserver_version}"")
-
-        check_neon_works(
-            env,
-            test_output_dir=test_output_dir,
-            sql_dump_path=compatibility_snapshot_dir / ""dump.sql"",
-            repo_dir=env.repo_dir,
-        )
+    env.start()
 
-    except Exception:
-        if breaking_changes_allowed:
-            pytest.xfail(
-                ""Breaking changes are allowed by ALLOW_FORWARD_COMPATIBILITY_BREAKAGE env var""
-            )
-        else:
-            raise
+    # ensure the specified pageserver is running
+    assert env.pageserver.log_contains(f""git(-env)?:{prev_pageserver_version}"")
 
-    assert not breaking_changes_allowed, (
-        ""Breaking changes are allowed by ALLOW_FORWARD_COMPATIBILITY_BREAKAGE, but the test has passed without any breakage""
+    check_neon_works(
+        env,
+        test_output_dir=test_output_dir,
+        sql_dump_path=compatibility_snapshot_dir / ""dump.sql"",
+        repo_dir=env.repo_dir,
     )
 
 