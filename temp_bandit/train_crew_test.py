@@ -5,7 +5,7 @@
 
 
 @mock.patch(""crewai.cli.train_crew.subprocess.run"")
-def test_train_crew_positive_iterations(mock_subprocess_run):
+def test_train_crew_positive_iterations(mock_subprocess_run) -> None:
     n_iterations = 5
     mock_subprocess_run.return_value = subprocess.CompletedProcess(
         args=[""uv"", ""run"", ""train"", str(n_iterations)],
@@ -25,7 +25,7 @@ def test_train_crew_positive_iterations(mock_subprocess_run):
 
 
 @mock.patch(""crewai.cli.train_crew.click"")
-def test_train_crew_zero_iterations(click):
+def test_train_crew_zero_iterations(click) -> None:
     train_crew(0, ""trained_agents_data.pkl"")
     click.echo.assert_called_once_with(
         ""An unexpected error occurred: The number of iterations must be a positive integer."",
@@ -34,7 +34,7 @@ def test_train_crew_zero_iterations(click):
 
 
 @mock.patch(""crewai.cli.train_crew.click"")
-def test_train_crew_negative_iterations(click):
+def test_train_crew_negative_iterations(click) -> None:
     train_crew(-2, ""trained_agents_data.pkl"")
     click.echo.assert_called_once_with(
         ""An unexpected error occurred: The number of iterations must be a positive integer."",
@@ -44,7 +44,7 @@ def test_train_crew_negative_iterations(click):
 
 @mock.patch(""crewai.cli.train_crew.click"")
 @mock.patch(""crewai.cli.train_crew.subprocess.run"")
-def test_train_crew_called_process_error(mock_subprocess_run, click):
+def test_train_crew_called_process_error(mock_subprocess_run, click) -> None:
     n_iterations = 5
     mock_subprocess_run.side_effect = subprocess.CalledProcessError(
         returncode=1,
@@ -67,13 +67,13 @@ def test_train_crew_called_process_error(mock_subprocess_run, click):
                 err=True,
             ),
             mock.call.echo(""Error"", err=True),
-        ]
+        ],
     )
 
 
 @mock.patch(""crewai.cli.train_crew.click"")
 @mock.patch(""crewai.cli.train_crew.subprocess.run"")
-def test_train_crew_unexpected_exception(mock_subprocess_run, click):
+def test_train_crew_unexpected_exception(mock_subprocess_run, click) -> None:
     n_iterations = 5
     mock_subprocess_run.side_effect = Exception(""Unexpected error"")
     train_crew(n_iterations, ""trained_agents_data.pkl"")
@@ -85,5 +85,5 @@ def test_train_crew_unexpected_exception(mock_subprocess_run, click):
         check=True,
     )
     click.echo.assert_called_once_with(
-        ""An unexpected error occurred: Unexpected error"", err=True
+        ""An unexpected error occurred: Unexpected error"", err=True,
     )