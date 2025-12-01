@@ -401,6 +401,15 @@ async def app_logs_pty(servicer, stream):
     assert captured.out.endswith(""
some data
\r"")
 
 
+def test_app_interactive_no_output(servicer, client):
+    app = App()
+
+    with pytest.warns(match=""Interactive mode is disabled because no output manager is active""):
+        with app.run(client=client, interactive=True):
+            # Verify that interactive mode was disabled
+            assert not app.is_interactive
+
+
 def test_show_progress_deprecations(client, monkeypatch):
     app = App()
 