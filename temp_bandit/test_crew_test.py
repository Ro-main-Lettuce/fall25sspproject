@@ -7,18 +7,18 @@
 
 
 @pytest.mark.parametrize(
-    ""n_iterations,model"",
+    (""n_iterations"", ""model""),
     [
         (1, ""gpt-4o""),
         (5, ""gpt-3.5-turbo""),
         (10, ""gpt-4""),
     ],
 )
 @mock.patch(""crewai.cli.evaluate_crew.subprocess.run"")
-def test_crew_success(mock_subprocess_run, n_iterations, model):
+def test_crew_success(mock_subprocess_run, n_iterations, model) -> None:
     """"""Test the crew function for successful execution.""""""
     mock_subprocess_run.return_value = subprocess.CompletedProcess(
-        args=f""uv run test {n_iterations} {model}"", returncode=0
+        args=f""uv run test {n_iterations} {model}"", returncode=0,
     )
     result = evaluate_crew.evaluate_crew(n_iterations, model)
 
@@ -32,7 +32,7 @@ def test_crew_success(mock_subprocess_run, n_iterations, model):
 
 
 @mock.patch(""crewai.cli.evaluate_crew.click"")
-def test_test_crew_zero_iterations(click):
+def test_test_crew_zero_iterations(click) -> None:
     evaluate_crew.evaluate_crew(0, ""gpt-4o"")
     click.echo.assert_called_once_with(
         ""An unexpected error occurred: The number of iterations must be a positive integer."",
@@ -41,7 +41,7 @@ def test_test_crew_zero_iterations(click):
 
 
 @mock.patch(""crewai.cli.evaluate_crew.click"")
-def test_test_crew_negative_iterations(click):
+def test_test_crew_negative_iterations(click) -> None:
     evaluate_crew.evaluate_crew(-2, ""gpt-4o"")
     click.echo.assert_called_once_with(
         ""An unexpected error occurred: The number of iterations must be a positive integer."",
@@ -51,7 +51,7 @@ def test_test_crew_negative_iterations(click):
 
 @mock.patch(""crewai.cli.evaluate_crew.click"")
 @mock.patch(""crewai.cli.evaluate_crew.subprocess.run"")
-def test_test_crew_called_process_error(mock_subprocess_run, click):
+def test_test_crew_called_process_error(mock_subprocess_run, click) -> None:
     n_iterations = 5
     mock_subprocess_run.side_effect = subprocess.CalledProcessError(
         returncode=1,
@@ -74,13 +74,13 @@ def test_test_crew_called_process_error(mock_subprocess_run, click):
                 err=True,
             ),
             mock.call.echo(""Error"", err=True),
-        ]
+        ],
     )
 
 
 @mock.patch(""crewai.cli.evaluate_crew.click"")
 @mock.patch(""crewai.cli.evaluate_crew.subprocess.run"")
-def test_test_crew_unexpected_exception(mock_subprocess_run, click):
+def test_test_crew_unexpected_exception(mock_subprocess_run, click) -> None:
     # Arrange
     n_iterations = 5
     mock_subprocess_run.side_effect = Exception(""Unexpected error"")
@@ -93,5 +93,5 @@ def test_test_crew_unexpected_exception(mock_subprocess_run, click):
         check=True,
     )
     click.echo.assert_called_once_with(
-        ""An unexpected error occurred: Unexpected error"", err=True
+        ""An unexpected error occurred: Unexpected error"", err=True,
     )