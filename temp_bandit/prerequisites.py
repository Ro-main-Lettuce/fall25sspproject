@@ -1370,28 +1370,25 @@ def check_running_mode(frontend: bool, backend: bool) -> tuple[bool, bool]:
     return frontend, backend
 
 
-def needs_reinit(frontend: bool = True) -> bool:
-    """"""Check if an app needs to be reinitialized.
-
-    Args:
-        frontend: Whether to check if the frontend is initialized.
-
-    Returns:
-        Whether the app needs to be reinitialized.
+def assert_in_reflex_dir():
+    """"""Assert that the current working directory is the reflex directory.
 
     Raises:
-        Exit: If the app is not initialized.
+        Exit: If the current working directory is not the reflex directory.
     """"""
     if not constants.Config.FILE.exists():
         console.error(
             f""[cyan]{constants.Config.FILE}[/cyan] not found. Move to the root folder of your project, or run [bold]{constants.Reflex.MODULE_NAME} init[/bold] to start a new project.""
         )
         raise click.exceptions.Exit(1)
 
-    # Don't need to reinit if not running in frontend mode.
-    if not frontend:
-        return False
 
+def needs_reinit() -> bool:
+    """"""Check if an app needs to be reinitialized.
+
+    Returns:
+        Whether the app needs to be reinitialized.
+    """"""
     # Make sure the .reflex directory exists.
     if not environment.REFLEX_DIR.get().exists():
         return True