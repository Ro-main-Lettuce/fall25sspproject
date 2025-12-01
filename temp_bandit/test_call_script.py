@@ -204,7 +204,10 @@ def reset_(self):
             self.reset()
 
     app = rx.App()
-    Path(""assets/external.js"").write_text(external_scripts)
+    external_scripts_path = Path(""assets/external.js"")
+    if not external_scripts_path.exists():
+        external_scripts_path.parent.mkdir(parents=True, exist_ok=True)
+        external_scripts_path.write_text(external_scripts)
 
     @app.add_page
     def index():