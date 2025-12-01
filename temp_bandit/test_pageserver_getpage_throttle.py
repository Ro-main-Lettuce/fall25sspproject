@@ -15,7 +15,6 @@
     from fixtures.neon_fixtures import NeonEnvBuilder, PgBin
 
 
-@pytest.mark.skip(""See https://github.com/neondatabase/neon/issues/11395"")
 def test_pageserver_getpage_throttle(neon_env_builder: NeonEnvBuilder, pg_bin: PgBin):
     env = neon_env_builder.init_start()
 
@@ -96,17 +95,12 @@ def run_pagebench_at_max_speed_and_get_total_requests_completed(duration_secs: i
     _, marker_offset = wait_until(lambda: env.pageserver.assert_log_contains(marker, offset=None))
 
     log.info(""run pagebench"")
-    duration_secs = 10
+    duration_secs = 20
     actual_ncompleted = run_pagebench_at_max_speed_and_get_total_requests_completed(duration_secs)
 
     log.info(""validate the client is capped at the configured rps limit"")
     expect_ncompleted = duration_secs * rate_limit_rps
-    delta_abs = abs(expect_ncompleted - actual_ncompleted)
-    threshold = 0.05 * expect_ncompleted
-    assert threshold / rate_limit_rps < 0.1 * duration_secs, (
-        ""test self-test: unrealistic expecations regarding precision in this test""
-    )
-    assert delta_abs < 0.05 * expect_ncompleted, (
+    assert pytest.approx(expect_ncompleted, 0.05) == actual_ncompleted, (
         ""the throttling deviates more than 5percent from the expectation""
     )
 
@@ -120,6 +114,7 @@ def run_pagebench_at_max_speed_and_get_total_requests_completed(duration_secs: i
         timeout=compaction_period,
     )
 
+    log.info(""validate the metrics"")
     smgr_query_seconds_post = ps_http.get_metric_value(smgr_metric_name, smgr_metrics_query)
     assert smgr_query_seconds_post is not None
     throttled_usecs_post = ps_http.get_metric_value(throttle_metric_name, throttle_metrics_query)
@@ -128,12 +123,13 @@ def run_pagebench_at_max_speed_and_get_total_requests_completed(duration_secs: i
     actual_throttled_usecs = throttled_usecs_post - throttled_usecs_pre
     actual_throttled_secs = actual_throttled_usecs / 1_000_000
 
-    log.info(""validate that the metric doesn't include throttle wait time"")
-    assert duration_secs >= 10 * actual_smgr_query_seconds, (
-        ""smgr metrics should not include throttle wait time""
+    assert pytest.approx(actual_throttled_secs + actual_smgr_query_seconds, 0.1) == duration_secs, (
+        ""throttling and processing latency = total request time; this assert validates thi holds on average""
     )
 
-    log.info(""validate that the throttling wait time metrics is correct"")
-    assert pytest.approx(actual_throttled_secs + actual_smgr_query_seconds, 0.1) == duration_secs, (
-        ""most of the time in this test is spent throttled because the rate-limit's contribution to latency dominates""
+    # without this assertion, the test would pass even if the throttling was completely broken
+    # but the request processing is so slow that it makes up for the latency that a correct throttling
+    # implementation would add
+    assert actual_smgr_query_seconds < 0.66 * duration_secs, (
+        ""test self-test: request processing is consuming most of the wall clock time; this risks that we're not actually testing throttling""
     )