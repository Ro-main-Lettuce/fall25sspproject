@@ -151,8 +151,10 @@ def _run(
     if not frontend and backend:
         _skip_compile()
 
+    prerequisites.assert_in_reflex_dir()
+
     # Check that the app is initialized.
-    if prerequisites.needs_reinit(frontend=frontend):
+    if frontend and prerequisites.needs_reinit():
         _init(name=config.app_name)
 
     # Delete the states folder if it exists.
@@ -403,19 +405,21 @@ def export(
 
     environment.REFLEX_COMPILE_CONTEXT.set(constants.CompileContext.EXPORT)
 
-    frontend_only, backend_only = prerequisites.check_running_mode(
+    should_frontend_run, should_backend_run = prerequisites.check_running_mode(
         frontend_only, backend_only
     )
 
     config = get_config()
 
-    if prerequisites.needs_reinit(frontend=frontend_only or not backend_only):
+    prerequisites.assert_in_reflex_dir()
+
+    if should_frontend_run and prerequisites.needs_reinit():
         _init(name=config.app_name)
 
     export_utils.export(
         zipping=zip,
-        frontend=frontend_only,
-        backend=backend_only,
+        frontend=should_frontend_run,
+        backend=should_backend_run,
         zip_dest_dir=zip_dest_dir,
         upload_db_file=upload_db_file,
         env=constants.Env.DEV if env == constants.Env.DEV else constants.Env.PROD,
@@ -631,8 +635,10 @@ def deploy(
     if interactive:
         dependency.check_requirements()
 
+    prerequisites.assert_in_reflex_dir()
+
     # Check if we are set up.
-    if prerequisites.needs_reinit(frontend=True):
+    if prerequisites.needs_reinit():
         _init(name=config.app_name)
     prerequisites.check_latest_package_version(constants.ReflexHostingCLI.MODULE_NAME)
 