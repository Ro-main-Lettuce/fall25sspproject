@@ -28,9 +28,10 @@ def test_create_success(mock_subprocess):
     with in_temp_dir():
         tool_command = ToolCommand()
 
-        with patch.object(tool_command, ""login"") as mock_login, patch(
-            ""sys.stdout"", new=StringIO()
-        ) as fake_out:
+        with (
+            patch.object(tool_command, ""login"") as mock_login,
+            patch(""sys.stdout"", new=StringIO()) as fake_out,
+        ):
             tool_command.create(""test-tool"")
             output = fake_out.getvalue()
 
@@ -82,7 +83,7 @@ def test_install_success(mock_get, mock_subprocess_run):
         capture_output=False,
         text=True,
         check=True,
-        env=unittest.mock.ANY
+        env=unittest.mock.ANY,
     )
 
     assert ""Successfully installed sample-tool"" in output