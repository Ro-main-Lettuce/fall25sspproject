@@ -798,13 +798,43 @@ def test_cli_run_sandbox_prompt_yes() -> None:
     p.kill()
 
 
-def test_shell_completion() -> None:
+# shell-completion has 1 input (value of $SHELL) & 3 outputs (return code, stdout, & stderr)
+# parameterize to give coverage. We use a boolean to specify if output on that stream should be present.
+@pytest.mark.parametrize(
+    ""shell,rc,expect_stdout,expect_stderr"".split("",""),
+    [
+        # valid shell values, rc of 0, data only on stdout
+        (""bash"", 0, True, False),
+        (""bash.exe"", 0, True, False),
+        (""/usr/bin/zsh"", 0, True, False),
+        pytest.param(
+            r""c:\spam\eggs\fish.exe"",
+            0,
+            True,
+            False,
+            marks=pytest.mark.skipif(
+                not sys.platform.startswith((""win32"", ""cygwin"")),
+                reason=""win32 only"",
+            ),
+        ),
+        # invalid shell values, rc of 0, data only on stderr
+        # (N.B. rc will become 2 when Issue #3476 is fixed)
+        (""bogus"", 0, False, True),
+    ],
+)
+def test_shell_completion(
+    shell: str, rc: int, expect_stdout: bool, expect_stderr: bool
+) -> None:
+    test_env = os.environ.copy()
+    test_env[""SHELL""] = shell
     p = subprocess.run(
         [""marimo"", ""shell-completion""],
         capture_output=True,
+        env=test_env,
     )
-    assert p.returncode == 0
-    assert p.stdout is not None
+    assert p.returncode == rc
+    assert bool(len(p.stdout)) == expect_stdout
+    assert bool(len(p.stderr)) == expect_stderr
 
 
 HAS_DOCKER = DependencyManager.which(""docker"")