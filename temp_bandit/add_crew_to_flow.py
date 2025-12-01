@@ -9,18 +9,18 @@ def add_crew_to_flow(crew_name: str) -> None:
     """"""Add a new crew to the current flow.""""""
     # Check if pyproject.toml exists in the current directory
     if not Path(""pyproject.toml"").exists():
-        print(""This command must be run from the root of a flow project."")
+        msg = ""This command must be run from the root of a flow project.""
         raise click.ClickException(
-            ""This command must be run from the root of a flow project.""
+            msg,
         )
 
     # Determine the flow folder based on the current directory
     flow_folder = Path.cwd()
     crews_folder = flow_folder / ""src"" / flow_folder.name / ""crews""
 
     if not crews_folder.exists():
-        print(""Crews folder does not exist in the current flow."")
-        raise click.ClickException(""Crews folder does not exist in the current flow."")
+        msg = ""Crews folder does not exist in the current flow.""
+        raise click.ClickException(msg)
 
     # Create the crew within the flow's crews directory
     create_embedded_crew(crew_name, parent_folder=crews_folder)
@@ -39,7 +39,7 @@ def create_embedded_crew(crew_name: str, parent_folder: Path) -> None:
 
     if crew_folder.exists():
         if not click.confirm(
-            f""Crew {folder_name} already exists. Do you want to override it?""
+            f""Crew {folder_name} already exists. Do you want to override it?"",
         ):
             click.secho(""Operation cancelled."", fg=""yellow"")
             return
@@ -66,5 +66,5 @@ def create_embedded_crew(crew_name: str, parent_folder: Path) -> None:
     copy_template(src_file, dst_file, crew_name, class_name, folder_name)
 
     click.secho(
-        f""Crew {crew_name} added to the flow successfully!"", fg=""green"", bold=True
+        f""Crew {crew_name} added to the flow successfully!"", fg=""green"", bold=True,
     )