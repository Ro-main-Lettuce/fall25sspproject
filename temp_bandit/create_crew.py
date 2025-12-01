@@ -24,7 +24,7 @@ def create_folder_structure(name, parent_folder=None):
 
     if folder_path.exists():
         if not click.confirm(
-            f""Folder {folder_name} already exists. Do you want to override it?""
+            f""Folder {folder_name} already exists. Do you want to override it?"",
         ):
             click.secho(""Operation cancelled."", fg=""yellow"")
             sys.exit(0)
@@ -48,7 +48,7 @@ def create_folder_structure(name, parent_folder=None):
     return folder_path, folder_name, class_name
 
 
-def copy_template_files(folder_path, name, class_name, parent_folder):
+def copy_template_files(folder_path, name, class_name, parent_folder) -> None:
     package_dir = Path(__file__).parent
     templates_dir = package_dir / ""templates"" / ""crew""
 
@@ -89,7 +89,7 @@ def copy_template_files(folder_path, name, class_name, parent_folder):
             copy_template(src_file, dst_file, name, class_name, folder_path.name)
 
 
-def create_crew(name, provider=None, skip_provider=False, parent_folder=None):
+def create_crew(name, provider=None, skip_provider=False, parent_folder=None) -> None:
     folder_path, folder_name, class_name = create_folder_structure(name, parent_folder)
     env_vars = load_env_vars(folder_path)
     if not skip_provider:
@@ -109,7 +109,7 @@ def create_crew(name, provider=None, skip_provider=False, parent_folder=None):
 
         if existing_provider:
             if not click.confirm(
-                f""Found existing environment variable configuration for {existing_provider.capitalize()}. Do you want to override it?""
+                f""Found existing environment variable configuration for {existing_provider.capitalize()}. Do you want to override it?"",
             ):
                 click.secho(""Keeping existing provider configuration."", fg=""yellow"")
                 return
@@ -126,11 +126,11 @@ def create_crew(name, provider=None, skip_provider=False, parent_folder=None):
             if selected_provider:  # Valid selection
                 break
             click.secho(
-                ""No provider selected. Please try again or press 'q' to exit."", fg=""red""
+                ""No provider selected. Please try again or press 'q' to exit."", fg=""red"",
             )
 
         # Check if the selected provider has predefined models
-        if selected_provider in MODELS and MODELS[selected_provider]:
+        if MODELS.get(selected_provider):
             while True:
                 selected_model = select_model(selected_provider, provider_models)
                 if selected_model is None:  # User typed 'q'
@@ -167,7 +167,7 @@ def create_crew(name, provider=None, skip_provider=False, parent_folder=None):
             click.secho(""API keys and model saved to .env file"", fg=""green"")
         else:
             click.secho(
-                ""No API keys provided. Skipping .env file creation."", fg=""yellow""
+                ""No API keys provided. Skipping .env file creation."", fg=""yellow"",
             )
 
         click.secho(f""Selected model: {env_vars.get('MODEL', 'N/A')}"", fg=""green"")