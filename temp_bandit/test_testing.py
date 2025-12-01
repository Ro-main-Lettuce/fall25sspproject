@@ -23,18 +23,16 @@ def BasicApp():
         class State(rx.State):
             pass
 
-        app = rx.App(_state=State)
+        app = rx.App()
         app.add_page(lambda: rx.text(""Basic App""), route=""/"", title=""index"")
-        app._compile()
 
     with AppHarness.create(
         root=tmp_path,
         app_source=BasicApp,
     ) as harness:
         assert harness.app_instance is not None
-        assert harness.backend is not None
         assert harness.frontend_url is not None
-        assert harness.frontend_process is not None
-        assert harness.frontend_process.poll() is None
+        assert harness.reflex_process is not None
+        assert harness.reflex_process.poll() is None
 
-    assert harness.frontend_process.poll() is not None
+    assert harness.reflex_process.poll() is not None