@@ -3,7 +3,6 @@
 from typing import TYPE_CHECKING
 
 import pytest
-import requests
 from fixtures.benchmark_fixture import MetricReport, NeonBenchmarker
 
 if TYPE_CHECKING:
@@ -68,9 +67,7 @@ def test_compute_startup_simple(
             endpoint.safe_psql(""select 1;"")
 
         # Get metrics
-        metrics = requests.get(
-            f""http://localhost:{endpoint.external_http_port}/metrics.json""
-        ).json()
+        metrics = endpoint.http_client().metrics_json()
         durations = {
             ""wait_for_spec_ms"": f""{i}_wait_for_spec"",
             ""sync_safekeepers_ms"": f""{i}_sync_safekeepers"",
@@ -155,9 +152,7 @@ def test_compute_ondemand_slru_startup(
             assert sum == 1000000
 
         # Get metrics
-        metrics = requests.get(
-            f""http://localhost:{endpoint.external_http_port}/metrics.json""
-        ).json()
+        metrics = endpoint.http_client().metrics_json()
         durations = {
             ""wait_for_spec_ms"": f""{slru}_{i}_wait_for_spec"",
             ""sync_safekeepers_ms"": f""{slru}_{i}_sync_safekeepers"",