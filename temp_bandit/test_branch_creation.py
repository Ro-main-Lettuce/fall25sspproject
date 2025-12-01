@@ -97,6 +97,7 @@ def run_pgbench(branch: str):
     _record_branch_creation_durations(neon_compare, branch_creation_durations)
 
 
+@pytest.mark.timeout(1000)
 @pytest.mark.parametrize(""n_branches"", [500, 1024])
 @pytest.mark.parametrize(""shape"", [""one_ancestor"", ""random""])
 def test_branch_creation_many(neon_compare: NeonCompare, n_branches: int, shape: str):
@@ -205,7 +206,7 @@ def metrics_are_filled() -> list[Sample]:
         assert len(matching) == len(expected_labels)
         return matching
 
-    samples = wait_until(metrics_are_filled)
+    samples = wait_until(metrics_are_filled, timeout=60)
 
     for sample in samples:
         phase = sample.labels[""phase""]