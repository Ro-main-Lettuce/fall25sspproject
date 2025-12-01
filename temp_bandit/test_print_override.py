@@ -25,7 +25,9 @@ def write(self, op: str, data: dict) -> None:
 class TestPrintOverride:
     def test_print_override_normal(self) -> None:
         # Test print_override when not in a marimo thread
-        with patch(""marimo._messaging.print_override._original_print"") as mock_print:
+        with patch(
+            ""marimo._messaging.print_override._original_print""
+        ) as mock_print:
             print_override(""Hello, world!"")
             mock_print.assert_called_once_with(""Hello, world!"")
 
@@ -35,7 +37,9 @@ def test_print_override_with_thread_no_context(self) -> None:
         THREADS.add(thread_id)
 
         try:
-            with patch(""marimo._messaging.print_override._original_print"") as mock_print:
+            with patch(
+                ""marimo._messaging.print_override._original_print""
+            ) as mock_print:
                 with patch(
                     ""marimo._messaging.print_override.get_context"",
                     side_effect=ContextNotInitializedError,
@@ -63,7 +67,9 @@ def test_print_override_with_thread_and_context(self) -> None:
             context.execution_context = MagicMock(spec=ExecutionContext)
             context.execution_context.cell_id = ""cell1""
 
-            with patch(""marimo._messaging.print_override._original_print"") as mock_print:
+            with patch(
+                ""marimo._messaging.print_override._original_print""
+            ) as mock_print:
                 with patch(
                     ""marimo._messaging.print_override.get_context"",
                     return_value=context,
@@ -77,9 +83,17 @@ def test_print_override_with_thread_and_context(self) -> None:
                     assert len(stream.messages) == 1
                     assert stream.messages[0][0] == ""cell-op""  # op
                     assert stream.messages[0][1][""cell_id""] == ""cell1""
-                    assert stream.messages[0][1][""console""][""channel""] == ""stdout""
-                    assert stream.messages[0][1][""console""][""mimetype""] == ""text/plain""
-                    assert stream.messages[0][1][""console""][""data""] == ""Hello, world!
""
+                    assert (
+                        stream.messages[0][1][""console""][""channel""] == ""stdout""
+                    )
+                    assert (
+                        stream.messages[0][1][""console""][""mimetype""]
+                        == ""text/plain""
+                    )
+                    assert (
+                        stream.messages[0][1][""console""][""data""]
+                        == ""Hello, world!
""
+                    )
         finally:
             # Clean up
             if thread_id in THREADS:
@@ -95,7 +109,9 @@ def test_print_override_with_thread_no_execution_context(self) -> None:
             context = MagicMock(spec=RuntimeContext)
             context.execution_context = None
 
-            with patch(""marimo._messaging.print_override._original_print"") as mock_print:
+            with patch(
+                ""marimo._messaging.print_override._original_print""
+            ) as mock_print:
                 with patch(
                     ""marimo._messaging.print_override.get_context"",
                     return_value=context,
@@ -123,7 +139,9 @@ def test_print_override_with_custom_sep_and_end(self) -> None:
             context.execution_context = MagicMock(spec=ExecutionContext)
             context.execution_context.cell_id = ""cell1""
 
-            with patch(""marimo._messaging.print_override._original_print"") as mock_print:
+            with patch(
+                ""marimo._messaging.print_override._original_print""
+            ) as mock_print:
                 with patch(
                     ""marimo._messaging.print_override.get_context"",
                     return_value=context,
@@ -135,7 +153,10 @@ def test_print_override_with_custom_sep_and_end(self) -> None:
 
                     # Message should be sent to the stream with custom sep and end
                     assert len(stream.messages) == 1
-                    assert stream.messages[0][1][""console""][""data""] == ""Hello-world!""
+                    assert (
+                        stream.messages[0][1][""console""][""data""]
+                        == ""Hello-world!""
+                    )
         finally:
             # Clean up
             if thread_id in THREADS:
@@ -155,7 +176,9 @@ def test_print_override_with_multiple_args(self) -> None:
             context.execution_context = MagicMock(spec=ExecutionContext)
             context.execution_context.cell_id = ""cell1""
 
-            with patch(""marimo._messaging.print_override._original_print"") as mock_print:
+            with patch(
+                ""marimo._messaging.print_override._original_print""
+            ) as mock_print:
                 with patch(
                     ""marimo._messaging.print_override.get_context"",
                     return_value=context,
@@ -167,7 +190,10 @@ def test_print_override_with_multiple_args(self) -> None:
 
                     # Message should be sent to the stream with all args converted to strings
                     assert len(stream.messages) == 1
-                    assert stream.messages[0][1][""console""][""data""] == ""Hello 123 True None
""
+                    assert (
+                        stream.messages[0][1][""console""][""data""]
+                        == ""Hello 123 True None
""
+                    )
         finally:
             # Clean up
             if thread_id in THREADS: