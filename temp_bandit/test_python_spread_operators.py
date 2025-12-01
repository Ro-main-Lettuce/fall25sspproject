@@ -16,6 +16,7 @@ def test_python_spread_operators(tmpdir) -> None:
 
         # Get the statement (PyDict) from the params assignment
         params_dict = params.value
+        assert params_dict is not None
 
         # Check that we can access the regular key-value pairs
         assert params_dict[""a""] == ""1""