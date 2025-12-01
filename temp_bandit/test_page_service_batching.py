@@ -1,5 +1,7 @@
+import concurrent.futures
 import dataclasses
 import json
+import threading
 import time
 from dataclasses import dataclass
 from pathlib import Path
@@ -28,38 +30,33 @@ class PageServicePipeliningConfigSerial(PageServicePipeliningConfig):
 class PageServicePipeliningConfigPipelined(PageServicePipeliningConfig):
     max_batch_size: int
     execution: str
+    batching: str
     mode: str = ""pipelined""
 
 
-EXECUTION = [""concurrent-futures"", ""tasks""]
+EXECUTION = [""concurrent-futures""]
+BATCHING = [""uniform-lsn"", ""scattered-lsn""]
 
 NON_BATCHABLE: list[PageServicePipeliningConfig] = [PageServicePipeliningConfigSerial()]
 for max_batch_size in [1, 32]:
     for execution in EXECUTION:
-        NON_BATCHABLE.append(PageServicePipeliningConfigPipelined(max_batch_size, execution))
+        for batching in BATCHING:
+            NON_BATCHABLE.append(
+                PageServicePipeliningConfigPipelined(max_batch_size, execution, batching)
+            )
 
-BATCHABLE: list[PageServicePipeliningConfig] = [PageServicePipeliningConfigSerial()]
-for max_batch_size in [1, 2, 4, 8, 16, 32]:
+BATCHABLE: list[PageServicePipeliningConfig] = []
+for max_batch_size in [32]:
     for execution in EXECUTION:
-        BATCHABLE.append(PageServicePipeliningConfigPipelined(max_batch_size, execution))
+        for batching in BATCHING:
+            BATCHABLE.append(
+                PageServicePipeliningConfigPipelined(max_batch_size, execution, batching)
+            )
 
 
 @pytest.mark.parametrize(
     ""tablesize_mib, pipelining_config, target_runtime, effective_io_concurrency, readhead_buffer_size, name"",
     [
-        # non-batchable workloads
-        # (A separate benchmark will consider latency).
-        *[
-            (
-                50,
-                config,
-                TARGET_RUNTIME,
-                1,
-                128,
-                f""not batchable {dataclasses.asdict(config)}"",
-            )
-            for config in NON_BATCHABLE
-        ],
         # batchable workloads should show throughput and CPU efficiency improvements
         *[
             (
@@ -137,7 +134,14 @@ def test_throughput(
 
     env = neon_env_builder.init_start()
     ps_http = env.pageserver.http_client()
-    endpoint = env.endpoints.create_start(""main"")
+    endpoint = env.endpoints.create_start(
+        ""main"",
+        config_lines=[
+            # minimal lfc & small shared buffers to force requests to pageserver
+            ""neon.max_file_cache_size=1MB"",
+            ""shared_buffers=10MB"",
+        ],
+    )
     conn = endpoint.connect()
     cur = conn.cursor()
 
@@ -155,7 +159,6 @@ def test_throughput(
     tablesize = tablesize_mib * 1024 * 1024
     npages = tablesize // (8 * 1024)
     cur.execute(""INSERT INTO t SELECT generate_series(1, %s)"", (npages,))
-    # TODO: can we force postgres to do sequential scans?
 
     #
     # Run the workload, collect `Metrics` before and after, calculate difference, normalize.
@@ -166,6 +169,7 @@ class Metrics:
         time: float
         pageserver_batch_size_histo_sum: float
         pageserver_batch_size_histo_count: float
+        pageserver_batch_breaks_reason_count: dict[str, int]
         compute_getpage_count: float
         pageserver_cpu_seconds_total: float
 
@@ -179,6 +183,10 @@ def __sub__(self, other: ""Metrics"") -> ""Metrics"":
                 compute_getpage_count=self.compute_getpage_count - other.compute_getpage_count,
                 pageserver_cpu_seconds_total=self.pageserver_cpu_seconds_total
                 - other.pageserver_cpu_seconds_total,
+                pageserver_batch_breaks_reason_count={
+                    reason: count - other.pageserver_batch_breaks_reason_count.get(reason, 0)
+                    for reason, count in self.pageserver_batch_breaks_reason_count.items()
+                },
             )
 
         def normalize(self, by) -> ""Metrics"":
@@ -188,6 +196,10 @@ def normalize(self, by) -> ""Metrics"":
                 pageserver_batch_size_histo_count=self.pageserver_batch_size_histo_count / by,
                 compute_getpage_count=self.compute_getpage_count / by,
                 pageserver_cpu_seconds_total=self.pageserver_cpu_seconds_total / by,
+                pageserver_batch_breaks_reason_count={
+                    reason: count / by
+                    for reason, count in self.pageserver_batch_breaks_reason_count.items()
+                },
             )
 
     def get_metrics() -> Metrics:
@@ -197,6 +209,20 @@ def get_metrics() -> Metrics:
             )
             compute_getpage_count = cur.fetchall()[0][0]
             pageserver_metrics = ps_http.get_metrics()
+            for name, samples in pageserver_metrics.metrics.items():
+                for sample in samples:
+                    log.info(f""{name=} labels={sample.labels} {sample.value}"")
+
+            raw_batch_break_reason_count = pageserver_metrics.query_all(
+                ""pageserver_page_service_batch_break_reason_total"",
+                filter={""timeline_id"": str(env.initial_timeline)},
+            )
+
+            batch_break_reason_count = {
+                sample.labels[""reason""]: int(sample.value)
+                for sample in raw_batch_break_reason_count
+            }
+
             return Metrics(
                 time=time.time(),
                 pageserver_batch_size_histo_sum=pageserver_metrics.query_one(
@@ -205,34 +231,58 @@ def get_metrics() -> Metrics:
                 pageserver_batch_size_histo_count=pageserver_metrics.query_one(
                     ""pageserver_page_service_batch_size_count""
                 ).value,
+                pageserver_batch_breaks_reason_count=batch_break_reason_count,
                 compute_getpage_count=compute_getpage_count,
                 pageserver_cpu_seconds_total=pageserver_metrics.query_one(
                     ""libmetrics_process_cpu_seconds_highres""
                 ).value,
             )
 
-    def workload() -> Metrics:
+    def workload(disruptor_started: threading.Event) -> Metrics:
+        disruptor_started.wait()
         start = time.time()
         iters = 0
         while time.time() - start < target_runtime or iters < 2:
-            log.info(""Seqscan %d"", iters)
             if iters == 1:
                 # round zero for warming up
                 before = get_metrics()
-            cur.execute(
-                ""select clear_buffer_cache()""
-            )  # TODO: what about LFC? doesn't matter right now because LFC isn't enabled by default in tests
             cur.execute(""select sum(data::bigint) from t"")
             assert cur.fetchall()[0][0] == npages * (npages + 1) // 2
             iters += 1
         after = get_metrics()
         return (after - before).normalize(iters - 1)
 
+    def disruptor(disruptor_started: threading.Event, stop_disruptor: threading.Event):
+        conn = endpoint.connect()
+        cur = conn.cursor()
+        iters = 0
+        while True:
+            cur.execute(""SELECT pg_logical_emit_message(true, 'test', 'advancelsn')"")
+            if stop_disruptor.is_set():
+                break
+            disruptor_started.set()
+            iters += 1
+            time.sleep(0.001)
+        return iters
+
     env.pageserver.patch_config_toml_nonrecursive(
         {""page_service_pipelining"": dataclasses.asdict(pipelining_config)}
     )
-    env.pageserver.restart()
-    metrics = workload()
+
+    # set trace for log analysis below
+    env.pageserver.restart(extra_env_vars={""RUST_LOG"": ""info,pageserver::page_service=trace""})
+
+    log.info(""Starting workload"")
+
+    with concurrent.futures.ThreadPoolExecutor() as executor:
+        disruptor_started = threading.Event()
+        stop_disruptor = threading.Event()
+        disruptor_fut = executor.submit(disruptor, disruptor_started, stop_disruptor)
+        workload_fut = executor.submit(workload, disruptor_started)
+        metrics = workload_fut.result()
+        stop_disruptor.set()
+        ndisruptions = disruptor_fut.result()
+        log.info(""Disruptor issued %d disrupting requests"", ndisruptions)
 
     log.info(""Results: %s"", metrics)
 
@@ -249,7 +299,16 @@ def workload() -> Metrics:
     #
 
     for metric, value in dataclasses.asdict(metrics).items():
-        zenbenchmark.record(f""counters.{metric}"", value, unit="""", report=MetricReport.TEST_PARAM)
+        if metric == ""pageserver_batch_breaks_reason_count"":
+            assert isinstance(value, dict)
+            for reason, count in value.items():
+                zenbenchmark.record(
+                    f""counters.{metric}_{reason}"", count, unit="""", report=MetricReport.TEST_PARAM
+                )
+        else:
+            zenbenchmark.record(
+                f""counters.{metric}"", value, unit="""", report=MetricReport.TEST_PARAM
+            )
 
     zenbenchmark.record(
         ""perfmetric.batching_factor"",
@@ -262,7 +321,10 @@ def workload() -> Metrics:
 PRECISION_CONFIGS: list[PageServicePipeliningConfig] = [PageServicePipeliningConfigSerial()]
 for max_batch_size in [1, 32]:
     for execution in EXECUTION:
-        PRECISION_CONFIGS.append(PageServicePipeliningConfigPipelined(max_batch_size, execution))
+        for batching in BATCHING:
+            PRECISION_CONFIGS.append(
+                PageServicePipeliningConfigPipelined(max_batch_size, execution, batching)
+            )
 
 
 @pytest.mark.parametrize(