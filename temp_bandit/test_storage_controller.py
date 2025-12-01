@@ -95,7 +95,7 @@ def test_storage_controller_smoke(
     env.pageservers[1].start()
     for sk in env.safekeepers:
         sk.start()
-    env.object_storage.start()
+    env.endpoint_storage.start()
 
     # The pageservers we started should have registered with the sharding service on startup
     nodes = env.storage_controller.node_list()
@@ -347,7 +347,7 @@ def prepare_onboarding_env(
     env = neon_env_builder.init_configs()
     env.broker.start()
     env.storage_controller.start()
-    env.object_storage.start()
+    env.endpoint_storage.start()
 
     # This is the pageserver where we'll initially create the tenant.  Run it in emergency
     # mode so that it doesn't talk to storage controller, and do not register it.
@@ -1612,16 +1612,18 @@ def test_storage_controller_heartbeats(
     env = neon_env_builder.init_configs()
     env.start()
 
-    # Default log allow list permits connection errors, but this test will use error responses on
-    # the utilization endpoint.
-    env.storage_controller.allowed_errors.append(
-        "".*Call to node.*management API.*failed.*failpoint.*""
-    )
-    # The server starts listening to the socket before sending re-attach request,
-    # but it starts serving HTTP only when re-attach is completed.
-    # If re-attach is slow (last scenario), storcon's heartbeat requests will time out.
-    env.storage_controller.allowed_errors.append(
-        "".*Call to node.*management API.*failed.* Timeout.*""
+    env.storage_controller.allowed_errors.extend(
+        [
+            # Default log allow list permits connection errors, but this test will use error responses on
+            # the utilization endpoint.
+            "".*Call to node.*management API.*failed.*failpoint.*"",
+            # The server starts listening to the socket before sending re-attach request,
+            # but it starts serving HTTP only when re-attach is completed.
+            # If re-attach is slow (last scenario), storcon's heartbeat requests will time out.
+            "".*Call to node.*management API.*failed.* Timeout.*"",
+            # We will intentionally cause reconcile errors
+            "".*Reconcile error.*"",
+        ]
     )
 
     # Initially we have two online pageservers
@@ -2892,10 +2894,12 @@ def new_becomes_leader():
         )
 
 
+@pytest.mark.parametrize(""step_down_times_out"", [False, True])
 def test_storage_controller_leadership_transfer_during_split(
     neon_env_builder: NeonEnvBuilder,
     storage_controller_proxy: StorageControllerProxy,
     port_distributor: PortDistributor,
+    step_down_times_out: bool,
 ):
     """"""
     Exercise a race between shard splitting and graceful leadership transfer.  This is
@@ -2936,13 +2940,33 @@ def test_storage_controller_leadership_transfer_during_split(
         )
     env.storage_controller.reconcile_until_idle()
 
+    # We are testing scenarios where the step down API does not complete: either because it is stuck
+    # doing a shard split, or because it totally times out on some other failpoint.
+    env.storage_controller.allowed_errors.extend(
+        [
+            "".*step_down.*request was dropped before completing.*"",
+            "".*step_down.*operation timed out.*"",
+            "".*Send step down request failed, will retry.*"",
+            "".*Send step down request still failed after.*retries.*"",
+            "".*Leader .+ did not respond to step-down request.*"",
+        ]
+    )
+
     with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
         # Start a shard split
         env.storage_controller.allowed_errors.extend(
             ["".*Unexpected child shard count.*"", "".*Enqueuing background abort.*""]
         )
         pause_failpoint = ""shard-split-pre-complete""
         env.storage_controller.configure_failpoints((pause_failpoint, ""pause""))
+
+        if not step_down_times_out:
+            # Prevent the timeout self-terminate code from executing: we will block step down on the
+            # shard split itself
+            env.storage_controller.configure_failpoints(
+                (""step-down-delay-timeout"", ""return(3600000)"")
+            )
+
         split_fut = executor.submit(
             env.storage_controller.tenant_shard_split, list(tenants)[0], shard_count * 2
         )
@@ -2961,12 +2985,20 @@ def hit_failpoint():
             timeout_in_seconds=30, instance_id=2, base_port=storage_controller_2_port
         )
 
+        if step_down_times_out:
+            # Step down will time out, original controller will terminate itself
+            env.storage_controller.allowed_errors.extend(["".*terminating process.*""])
+        else:
+            # Step down does not time out: original controller hits its shard split completion
+            # code path and realises that it must not purge the parent shards from the database.
+            env.storage_controller.allowed_errors.extend(["".*Enqueuing background abort.*""])
+
         def passed_split_abort():
             try:
                 log.info(""Checking log for pattern..."")
-                assert env.storage_controller.log_contains(
-                    "".*Using observed state received from leader.*""
-                )
+                # This log is indicative of entering startup_reconcile, which happens
+                # after the point we would abort shard splits
+                assert env.storage_controller.log_contains("".*Populating tenant shards.*"")
             except Exception:
                 log.exception(""Failed to find pattern in log"")
                 raise
@@ -2975,34 +3007,42 @@ def passed_split_abort():
         wait_until(passed_split_abort, interval=0.1, status_interval=1.0)
         assert env.storage_controller.log_contains("".*Aborting shard split.*"")
 
-        # Proxy is still talking to original controller here: disable its pause failpoint so
-        # that its shard split can run to completion.
-        log.info(""Disabling failpoint"")
-        # Bypass the proxy: the python test HTTPServer is single threaded and still blocked
-        # on handling the shard split request.
-        env.storage_controller.request(
-            ""PUT"",
-            f""http://127.0.0.1:{storage_controller_1_port}/debug/v1/failpoints"",
-            json=[{""name"": ""shard-split-pre-complete"", ""actions"": ""off""}],
-            headers=env.storage_controller.headers(TokenScope.ADMIN),
-        )
+        if step_down_times_out:
+            # We will let the old controller hit a timeout path where it terminates itself, rather than
+            # completing step_down and trying to complete a shard split
+            def old_controller_terminated():
+                assert env.storage_controller.log_contains("".*terminating process.*"")
 
-        def previous_stepped_down():
-            assert (
-                env.storage_controller.get_leadership_status()
-                == StorageControllerLeadershipStatus.STEPPED_DOWN
+            wait_until(old_controller_terminated)
+        else:
+            # Proxy is still talking to original controller here: disable its pause failpoint so
+            # that its shard split can run to completion.
+            log.info(""Disabling failpoint"")
+            # Bypass the proxy: the python test HTTPServer is single threaded and still blocked
+            # on handling the shard split request.
+            env.storage_controller.request(
+                ""PUT"",
+                f""http://127.0.0.1:{storage_controller_1_port}/debug/v1/failpoints"",
+                json=[{""name"": ""shard-split-pre-complete"", ""actions"": ""off""}],
+                headers=env.storage_controller.headers(TokenScope.ADMIN),
             )
 
-        log.info(""Awaiting step down"")
-        wait_until(previous_stepped_down)
+            def previous_stepped_down():
+                assert (
+                    env.storage_controller.get_leadership_status()
+                    == StorageControllerLeadershipStatus.STEPPED_DOWN
+                )
+
+            log.info(""Awaiting step down"")
+            wait_until(previous_stepped_down)
 
-        # Let the shard split complete: this may happen _after_ the replacement has come up
-        # and tried to clean up the databases
-        log.info(""Unblocking & awaiting shard split"")
-        with pytest.raises(Exception, match=""Unexpected child shard count""):
-            # This split fails when it tries to persist results, because it encounters
-            # changes already made by the new controller's abort-on-startup
-            split_fut.result()
+            # Let the shard split complete: this may happen _after_ the replacement has come up
+            # and tried to clean up the databases
+            log.info(""Unblocking & awaiting shard split"")
+            with pytest.raises(Exception, match=""Unexpected child shard count""):
+                # This split fails when it tries to persist results, because it encounters
+                # changes already made by the new controller's abort-on-startup
+                split_fut.result()
 
         log.info(""Routing to new leader"")
         storage_controller_proxy.route_to(f""http://127.0.0.1:{storage_controller_2_port}"")
@@ -3020,13 +3060,14 @@ def new_becomes_leader():
     env.storage_controller.wait_until_ready()
     env.storage_controller.consistency_check()
 
-    # Check that the stepped down instance forwards requests
-    # to the new leader while it's still running.
-    storage_controller_proxy.route_to(f""http://127.0.0.1:{storage_controller_1_port}"")
-    env.storage_controller.tenant_shard_dump()
-    env.storage_controller.node_configure(env.pageservers[0].id, {""scheduling"": ""Pause""})
-    status = env.storage_controller.node_status(env.pageservers[0].id)
-    assert status[""scheduling""] == ""Pause""
+    if not step_down_times_out:
+        # Check that the stepped down instance forwards requests
+        # to the new leader while it's still running.
+        storage_controller_proxy.route_to(f""http://127.0.0.1:{storage_controller_1_port}"")
+        env.storage_controller.tenant_shard_dump()
+        env.storage_controller.node_configure(env.pageservers[0].id, {""scheduling"": ""Pause""})
+        status = env.storage_controller.node_status(env.pageservers[0].id)
+        assert status[""scheduling""] == ""Pause""
 
 
 def test_storage_controller_ps_restarted_during_drain(neon_env_builder: NeonEnvBuilder):
@@ -4075,13 +4116,29 @@ def test_storage_controller_location_conf_equivalence(neon_env_builder: NeonEnvB
     assert reconciles_after_restart == 0
 
 
+class RestartStorcon(Enum):
+    RESTART = ""restart""
+    ONLINE = ""online""
+
+
+class DeletionSubject(Enum):
+    TIMELINE = ""timeline""
+    TENANT = ""tenant""
+
+
 @run_only_on_default_postgres(""PG version is not interesting here"")
-@pytest.mark.parametrize(""restart_storcon"", [True, False])
-def test_storcon_create_delete_sk_down(neon_env_builder: NeonEnvBuilder, restart_storcon: bool):
+@pytest.mark.parametrize(""restart_storcon"", [RestartStorcon.RESTART, RestartStorcon.ONLINE])
+@pytest.mark.parametrize(""deletetion_subject"", [DeletionSubject.TENANT, DeletionSubject.TIMELINE])
+def test_storcon_create_delete_sk_down(
+    neon_env_builder: NeonEnvBuilder,
+    restart_storcon: RestartStorcon,
+    deletetion_subject: DeletionSubject,
+):
     """"""
     Test that the storcon can create and delete tenants and timelines with a safekeeper being down.
-      - restart_storcon: tests whether the pending ops are persisted.
+      - restart_storcon: tests that the pending ops are persisted.
         if we don't restart, we test that we don't require it to come from the db.
+      - deletion_subject: test that both single timeline and whole tenant deletion work.
     """"""
 
     neon_env_builder.num_safekeepers = 3
@@ -4104,6 +4161,7 @@ def logged_offline():
     tenant_id = TenantId.generate()
     timeline_id = TimelineId.generate()
     env.create_tenant(tenant_id, timeline_id)
+    child_timeline_id = env.create_branch(""child_of_main"", tenant_id)
 
     env.safekeepers[1].assert_log_contains(f""creating new timeline {tenant_id}/{timeline_id}"")
     env.safekeepers[2].assert_log_contains(f""creating new timeline {tenant_id}/{timeline_id}"")
@@ -4116,7 +4174,7 @@ def logged_offline():
         ]
     )
 
-    if restart_storcon:
+    if restart_storcon == RestartStorcon.RESTART:
         # Restart the storcon to check that we persist operations
         env.storage_controller.stop()
         env.storage_controller.start()
@@ -4129,6 +4187,13 @@ def logged_offline():
         ep.start(safekeeper_generation=1, safekeepers=[1, 2, 3])
         ep.safe_psql(""CREATE TABLE IF NOT EXISTS t(key int, value text)"")
 
+    with env.endpoints.create(
+        ""child_of_main"", tenant_id=tenant_id, config_lines=config_lines
+    ) as ep:
+        # endpoint should start.
+        ep.start(safekeeper_generation=1, safekeepers=[1, 2, 3])
+        ep.safe_psql(""CREATE TABLE IF NOT EXISTS t(key int, value text)"")
+
     env.storage_controller.assert_log_contains(""writing pending op for sk id 1"")
     env.safekeepers[0].start()
 
@@ -4137,25 +4202,31 @@ def logged_contains_on_sk():
         env.safekeepers[0].assert_log_contains(
             f""pulling timeline {tenant_id}/{timeline_id} from safekeeper""
         )
+        env.safekeepers[0].assert_log_contains(
+            f""pulling timeline {tenant_id}/{child_timeline_id} from safekeeper""
+        )
 
     wait_until(logged_contains_on_sk)
 
     env.safekeepers[1].stop()
 
-    env.storage_controller.pageserver_api().tenant_delete(tenant_id)
+    if deletetion_subject == DeletionSubject.TENANT:
+        env.storage_controller.pageserver_api().tenant_delete(tenant_id)
+    else:
+        env.storage_controller.pageserver_api().timeline_delete(tenant_id, child_timeline_id)
 
     # ensure the safekeeper deleted the timeline
     def timeline_deleted_on_active_sks():
         env.safekeepers[0].assert_log_contains(
-            f""deleting timeline {tenant_id}/{timeline_id} from disk""
+            f""deleting timeline {tenant_id}/{child_timeline_id} from disk""
         )
         env.safekeepers[2].assert_log_contains(
-            f""deleting timeline {tenant_id}/{timeline_id} from disk""
+            f""deleting timeline {tenant_id}/{child_timeline_id} from disk""
         )
 
     wait_until(timeline_deleted_on_active_sks)
 
-    if restart_storcon:
+    if restart_storcon == RestartStorcon.RESTART:
         # Restart the storcon to check that we persist operations
         env.storage_controller.stop()
         env.storage_controller.start()
@@ -4165,7 +4236,64 @@ def timeline_deleted_on_active_sks():
     # ensure that there is log msgs for the third safekeeper too
     def timeline_deleted_on_sk():
         env.safekeepers[1].assert_log_contains(
-            f""deleting timeline {tenant_id}/{timeline_id} from disk""
+            f""deleting timeline {tenant_id}/{child_timeline_id} from disk""
+        )
+
+    wait_until(timeline_deleted_on_sk)
+
+
+@run_only_on_default_postgres(""PG version is not interesting here"")
+@pytest.mark.parametrize(""num_safekeepers"", [1, 2, 3])
+@pytest.mark.parametrize(""deletetion_subject"", [DeletionSubject.TENANT, DeletionSubject.TIMELINE])
+def test_storcon_few_sk(
+    neon_env_builder: NeonEnvBuilder,
+    num_safekeepers: int,
+    deletetion_subject: DeletionSubject,
+):
+    """"""
+    Test that the storcon can create and delete tenants and timelines with a limited/special number of safekeepers
+      - num_safekeepers: number of safekeepers.
+      - deletion_subject: test that both single timeline and whole tenant deletion work.
+    """"""
+
+    neon_env_builder.num_safekeepers = num_safekeepers
+    safekeeper_list = list(range(1, num_safekeepers + 1))
+    neon_env_builder.storage_controller_config = {
+        ""timelines_onto_safekeepers"": True,
+    }
+    env = neon_env_builder.init_start()
+
+    tenant_id = TenantId.generate()
+    timeline_id = TimelineId.generate()
+    env.create_tenant(tenant_id, timeline_id)
+    child_timeline_id = env.create_branch(""child_of_main"", tenant_id)
+
+    env.safekeepers[0].assert_log_contains(f""creating new timeline {tenant_id}/{timeline_id}"")
+
+    config_lines = [
+        ""neon.safekeeper_proto_version = 3"",
+    ]
+    with env.endpoints.create(""main"", tenant_id=tenant_id, config_lines=config_lines) as ep:
+        # endpoint should start.
+        ep.start(safekeeper_generation=1, safekeepers=safekeeper_list)
+        ep.safe_psql(""CREATE TABLE IF NOT EXISTS t(key int, value text)"")
+
+    with env.endpoints.create(
+        ""child_of_main"", tenant_id=tenant_id, config_lines=config_lines
+    ) as ep:
+        # endpoint should start.
+        ep.start(safekeeper_generation=1, safekeepers=safekeeper_list)
+        ep.safe_psql(""CREATE TABLE IF NOT EXISTS t(key int, value text)"")
+
+    if deletetion_subject is DeletionSubject.TENANT:
+        env.storage_controller.pageserver_api().tenant_delete(tenant_id)
+    else:
+        env.storage_controller.pageserver_api().timeline_delete(tenant_id, child_timeline_id)
+
+    # ensure that there is log msgs for the third safekeeper too
+    def timeline_deleted_on_sk():
+        env.safekeepers[0].assert_log_contains(
+            f""deleting timeline {tenant_id}/{child_timeline_id} from disk""
         )
 
     wait_until(timeline_deleted_on_sk)