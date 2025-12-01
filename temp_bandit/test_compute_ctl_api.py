@@ -41,24 +41,24 @@ def test_compute_ctl_api_latencies(
     zenbenchmark.record(
         ""status_response_latency_p50_us"",
         status_response_latency_us[len(status_response_latency_us) // 2],
-        ""microseconds"",
+        ""μs"",
         MetricReport.LOWER_IS_BETTER,
     )
     zenbenchmark.record(
         ""metrics_response_latency_p50_us"",
         metrics_response_latency_us[len(metrics_response_latency_us) // 2],
-        ""microseconds"",
+        ""μs"",
         MetricReport.LOWER_IS_BETTER,
     )
     zenbenchmark.record(
         ""status_response_latency_p99_us"",
         status_response_latency_us[len(status_response_latency_us) * 99 // 100],
-        ""microseconds"",
+        ""μs"",
         MetricReport.LOWER_IS_BETTER,
     )
     zenbenchmark.record(
         ""metrics_response_latency_p99_us"",
         metrics_response_latency_us[len(metrics_response_latency_us) * 99 // 100],
-        ""microseconds"",
+        ""μs"",
         MetricReport.LOWER_IS_BETTER,
     )