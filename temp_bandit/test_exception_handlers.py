@@ -3,7 +3,7 @@
 from __future__ import annotations
 
 import time
-from collections.abc import Generator
+from collections.abc import Callable, Generator
 
 import pytest
 from selenium.webdriver.common.by import By
@@ -13,8 +13,6 @@
 
 from reflex.testing import AppHarness, AppHarnessProd
 
-pytestmark = [pytest.mark.ignore_console_error]
-
 
 def TestApp():
     """"""A test app for event exception handler integration.""""""
@@ -86,6 +84,8 @@ def test_app(
         app_name=f""testapp_{app_harness_env.__name__.lower()}"",
         app_source=TestApp,
     ) as harness:
+        # disable console.error checking for this test
+        harness.reflex_process_error_log_path = None
         yield harness
 
 
@@ -108,9 +108,35 @@ def driver(test_app: AppHarness) -> Generator[WebDriver, None, None]:
         driver.quit()
 
 
+@pytest.fixture
+def get_reflex_output(test_app: AppHarness) -> Callable[[], str]:
+    """"""Get the output of the reflex process.
+
+    Args:
+        test_app: harness for TestApp app
+
+    Returns:
+        The output of the reflex process.
+    """"""
+    assert test_app.reflex_process is not None, ""app is not running""
+    assert test_app.reflex_process_log_path is not None, (
+        ""reflex process log path is not set""
+    )
+    initial_offset = test_app.reflex_process_log_path.stat().st_size
+
+    def f() -> str:
+        assert test_app.reflex_process_log_path is not None, (
+            ""reflex process log path is not set""
+        )
+        return test_app.reflex_process_log_path.read_bytes()[initial_offset:].decode(
+            ""utf-8""
+        )
+
+    return f
+
+
 def test_frontend_exception_handler_during_runtime(
-    driver: WebDriver,
-    capsys,
+    driver: WebDriver, get_reflex_output: Callable[[], str]
 ):
     """"""Test calling frontend exception handler during runtime.
 
@@ -119,7 +145,7 @@ def test_frontend_exception_handler_during_runtime(
 
     Args:
         driver: WebDriver instance.
-        capsys: pytest fixture for capturing stdout and stderr.
+        get_reflex_output: Function to get the reflex process output.
 
     """"""
     reset_button = WebDriverWait(driver, 20).until(
@@ -131,14 +157,14 @@ def test_frontend_exception_handler_during_runtime(
     # Wait for the error to be logged
     time.sleep(2)
 
-    captured_default_handler_output = capsys.readouterr()
-    assert ""induce_frontend_error"" in captured_default_handler_output.out
-    assert ""ReferenceError"" in captured_default_handler_output.out
+    captured_default_handler_output = get_reflex_output()
+    assert ""induce_frontend_error"" in captured_default_handler_output
+    assert ""ReferenceError"" in captured_default_handler_output
 
 
 def test_backend_exception_handler_during_runtime(
     driver: WebDriver,
-    capsys,
+    get_reflex_output: Callable[[], str],
 ):
     """"""Test calling backend exception handler during runtime.
 
@@ -147,7 +173,7 @@ def test_backend_exception_handler_during_runtime(
 
     Args:
         driver: WebDriver instance.
-        capsys: pytest fixture for capturing stdout and stderr.
+        get_reflex_output: Function to get the reflex process output.
 
     """"""
     reset_button = WebDriverWait(driver, 20).until(
@@ -159,15 +185,15 @@ def test_backend_exception_handler_during_runtime(
     # Wait for the error to be logged
     time.sleep(2)
 
-    captured_default_handler_output = capsys.readouterr()
-    assert ""divide_by_number"" in captured_default_handler_output.out
-    assert ""ZeroDivisionError"" in captured_default_handler_output.out
+    captured_default_handler_output = get_reflex_output()
+    assert ""divide_by_number"" in captured_default_handler_output
+    assert ""ZeroDivisionError"" in captured_default_handler_output
 
 
 def test_frontend_exception_handler_with_react(
     test_app: AppHarness,
     driver: WebDriver,
-    capsys,
+    get_reflex_output: Callable[[], str],
 ):
     """"""Test calling frontend exception handler during runtime.
 
@@ -176,7 +202,7 @@ def test_frontend_exception_handler_with_react(
     Args:
         test_app: harness for TestApp app
         driver: WebDriver instance.
-        capsys: pytest fixture for capturing stdout and stderr.
+        get_reflex_output: Function to get the reflex process output.
 
     """"""
     reset_button = WebDriverWait(driver, 20).until(
@@ -188,11 +214,11 @@ def test_frontend_exception_handler_with_react(
     # Wait for the error to be logged
     time.sleep(2)
 
-    captured_default_handler_output = capsys.readouterr()
+    captured_default_handler_output = get_reflex_output()
     if isinstance(test_app, AppHarnessProd):
-        assert ""Error: Minified React error #31"" in captured_default_handler_output.out
+        assert ""Error: Minified React error #31"" in captured_default_handler_output
     else:
         assert (
             ""Error: Objects are not valid as a React child (found: object with keys 
{invalid})""
-            in captured_default_handler_output.out
+            in captured_default_handler_output
         )