@@ -11,9 +11,8 @@ def update_crew() -> None:
     migrate_pyproject(""pyproject.toml"", ""pyproject.toml"")
 
 
-def migrate_pyproject(input_file, output_file):
-    """"""
-    Migrate the pyproject.toml to the new format.
+def migrate_pyproject(input_file, output_file) -> None:
+    """"""Migrate the pyproject.toml to the new format.
 
     This function is used to migrate the pyproject.toml to the new format.
     And it will be used to migrate the pyproject.toml to the new format when uv is used.
@@ -81,7 +80,7 @@ def migrate_pyproject(input_file, output_file):
         # Extract the module name from any existing script
         existing_scripts = new_pyproject[""project""][""scripts""]
         module_name = next(
-            (value.split(""."")[0] for value in existing_scripts.values() if ""."" in value)
+            value.split(""."")[0] for value in existing_scripts.values() if ""."" in value
         )
 
         new_pyproject[""project""][""scripts""][""run_crew""] = f""{module_name}.main:run""
@@ -93,22 +92,19 @@ def migrate_pyproject(input_file, output_file):
     # Backup the old pyproject.toml
     backup_file = ""pyproject-old.toml""
     shutil.copy2(input_file, backup_file)
-    print(f""Original pyproject.toml backed up as {backup_file}"")
 
     # Rename the poetry.lock file
     lock_file = ""poetry.lock""
     lock_backup = ""poetry-old.lock""
     if os.path.exists(lock_file):
         os.rename(lock_file, lock_backup)
-        print(f""Original poetry.lock renamed to {lock_backup}"")
     else:
-        print(""No poetry.lock file found to rename."")
+        pass
 
     # Write the new pyproject.toml
     with open(output_file, ""wb"") as f:
         tomli_w.dump(new_pyproject, f)
 
-    print(f""Migration complete. New pyproject.toml written to {output_file}"")
 
 
 def parse_version(version: str) -> str: