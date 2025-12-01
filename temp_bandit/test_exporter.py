@@ -296,16 +296,18 @@ def _():
     assert did_error is True
     cell_ops = [op for op in session_view.operations if isinstance(op, CellOp)]
 
-    # Skip snapshot comparison for Python 3.13 due to traceback format changes
+    # Use a version-specific snapshot for Python 3.13 due to traceback format changes
+    messages = _print_messages(cell_ops)
     if sys.version_info >= (3, 13):
-        # Python 3.13 has different traceback formatting, so we just verify error content
-        messages = _print_messages(cell_ops)
-        assert ""ValueError"" in messages
-        assert ""Failed to authenticate"" in messages
+        # Python 3.13 has different traceback formatting
+        snapshot(
+            ""run_until_completion_with_stack_trace_py313.txt"",
+            _delete_lines_with_files(messages),
+        )
     else:
         snapshot(
             ""run_until_completion_with_stack_trace.txt"",
-            _delete_lines_with_files(_print_messages(cell_ops)),
+            _delete_lines_with_files(messages),
         )
 
 