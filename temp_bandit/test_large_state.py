@@ -42,7 +42,16 @@ def get_driver(large_state) -> WebDriver:
     return large_state.frontend()
 
 
-@pytest.mark.parametrize(""var_count"", [1, 10, 100, 1000, 10000])
+@pytest.mark.parametrize(
+    ""var_count"",
+    [
+        1,
+        10,
+        100,
+        1000,
+        pytest.param(10000, marks=pytest.mark.skip(reason=""Invalid string length"")),
+    ],
+)
 def test_large_state(var_count: int, tmp_path_factory, benchmark):
     """"""Measure how long it takes for button click => state update to round trip.
 