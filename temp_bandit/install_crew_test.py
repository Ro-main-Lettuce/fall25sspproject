@@ -1,37 +1,39 @@
 from unittest import mock
+from typing import List, Any
 import pytest
 import subprocess
 
-from crewai.cli.install_crew import install_crew
+from crewai.cli.install_crew import install_crew, UV_COMMAND, SYNC_COMMAND, ACTIVE_FLAG
 
 
+@pytest.mark.parametrize(
+    ""proxy_options,expected_command"",
+    [
+        ([], [UV_COMMAND, SYNC_COMMAND, ACTIVE_FLAG]),
+        (
+            [""--index-url"", ""https://custom-pypi.org/simple""],
+            [UV_COMMAND, SYNC_COMMAND, ACTIVE_FLAG, ""--index-url"", ""https://custom-pypi.org/simple""],
+        ),
+    ],
+)
 @mock.patch(""subprocess.run"")
-def test_install_crew_with_active_flag(mock_subprocess):
-    """"""Test that install_crew includes the --active flag.""""""
-    install_crew([])
-    mock_subprocess.assert_called_once_with(
-        [""uv"", ""sync"", ""--active""], check=True, capture_output=False, text=True
-    )
-
-
-@mock.patch(""subprocess.run"")
-def test_install_crew_with_proxy_options(mock_subprocess):
-    """"""Test that install_crew correctly passes proxy options.""""""
-    proxy_options = [""--index-url"", ""https://custom-pypi.org/simple""]
+def test_install_crew_with_options(
+    mock_subprocess: mock.MagicMock, proxy_options: List[str], expected_command: List[str]
+) -> None:
+    """"""Test that install_crew correctly passes options to the command.""""""
     install_crew(proxy_options)
     mock_subprocess.assert_called_once_with(
-        [""uv"", ""sync"", ""--active"", ""--index-url"", ""https://custom-pypi.org/simple""],
-        check=True,
-        capture_output=False,
-        text=True,
+        expected_command, check=True, capture_output=False, text=True
     )
 
 
 @mock.patch(""subprocess.run"")
 @mock.patch(""click.echo"")
-def test_install_crew_with_subprocess_error(mock_echo, mock_subprocess):
+def test_install_crew_with_subprocess_error(
+    mock_echo: mock.MagicMock, mock_subprocess: mock.MagicMock
+) -> None:
     """"""Test that install_crew handles subprocess errors correctly.""""""
-    error = subprocess.CalledProcessError(1, ""uv sync --active"")
+    error = subprocess.CalledProcessError(1, f""{UV_COMMAND} {SYNC_COMMAND} {ACTIVE_FLAG}"")
     error.output = ""Error output""
     mock_subprocess.side_effect = error
     
@@ -44,11 +46,34 @@ def test_install_crew_with_subprocess_error(mock_echo, mock_subprocess):
 
 @mock.patch(""subprocess.run"")
 @mock.patch(""click.echo"")
-def test_install_crew_with_generic_exception(mock_echo, mock_subprocess):
+def test_install_crew_with_subprocess_error_empty_output(
+    mock_echo: mock.MagicMock, mock_subprocess: mock.MagicMock
+) -> None:
+    """"""Test that install_crew handles subprocess errors with empty output correctly.""""""
+    error = subprocess.CalledProcessError(1, f""{UV_COMMAND} {SYNC_COMMAND} {ACTIVE_FLAG}"")
+    error.output = None
+    mock_subprocess.side_effect = error
+    
+    install_crew([])
+    
+    mock_echo.assert_called_once_with(f""An error occurred while running the crew: {error}"", err=True)
+
+
+@mock.patch(""subprocess.run"")
+@mock.patch(""click.echo"")
+def test_install_crew_with_generic_exception(
+    mock_echo: mock.MagicMock, mock_subprocess: mock.MagicMock
+) -> None:
     """"""Test that install_crew handles generic exceptions correctly.""""""
     error = Exception(""Generic error"")
     mock_subprocess.side_effect = error
     
     install_crew([])
     
     mock_echo.assert_called_once_with(f""An unexpected error occurred: {error}"", err=True)
+
+
+def test_install_crew_with_invalid_proxy_options() -> None:
+    """"""Test that install_crew validates the proxy_options parameter.""""""
+    with pytest.raises(ValueError, match=""proxy_options must be a list""):
+        install_crew(""not a list"")  # type: ignore