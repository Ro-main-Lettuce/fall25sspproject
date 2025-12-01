@@ -34,95 +34,63 @@ def convert_file_to_url(file_path):
     
     return ""/docs/"" + ""/"".join(url_parts) + ""/""
 
+def build_url_to_filepath_mapping():
+    """"""Build dynamic mapping from browser URLs to filesystem paths.
+    
+    Uses the same logic as the main docpage.py function.
+    """"""
+    import flexdown
+    import reflex as rx
+    
+    url_to_filepath = {}
+    
+    flexdown_docs = [
+        str(doc).replace(""\\"", ""/"") for doc in flexdown.utils.get_flexdown_files(""docs/"")
+    ]
+    
+    for doc_path in flexdown_docs:
+        browser_url = rx.utils.format.to_kebab_case(f""/{doc_path.replace('.md', '/')}"")
+        
+        if browser_url.endswith(""/index/""):
+            folder_url = browser_url[:-7] + ""/""
+            index_url = browser_url[:-1]  # Remove trailing slash but keep /index
+            
+            folder_key = folder_url.strip(""/"")
+            index_key = index_url.strip(""/"")
+            
+            if folder_key.startswith(""docs/""):
+                folder_key = folder_key[5:]
+            if index_key.startswith(""docs/""):
+                index_key = index_key[5:]
+            
+            url_to_filepath[folder_key] = doc_path
+            url_to_filepath[index_key] = doc_path
+        else:
+            url_key = browser_url.strip(""/"")
+            if url_key.startswith(""docs/""):
+                url_key = url_key[5:]
+            
+            url_to_filepath[url_key] = doc_path
+    
+    return url_to_filepath
+
 def convert_url_to_github_path(url_path):
-    """"""Convert URL path to GitHub file path using the same logic as the app.""""""
+    """"""Convert URL path to GitHub file path using dynamic mapping.""""""
+    url_to_filepath_map = build_url_to_filepath_mapping()
+    
     path = str(url_path).strip(""/"")
     while ""//"" in path:
         path = path.replace(""//"", ""/"")
     
-    path = path.replace(""getting-started"", ""getting_started"")
-    path = path.replace(""client-storage"", ""client_storage"")
-    path = path.replace(""utility-methods"", ""utility_methods"")
-    path = path.replace(""advanced-onboarding"", ""advanced_onboarding"")
-    path = path.replace(""state-structure"", ""state_structure"")
-    path = path.replace(""ai-builder"", ""ai_builder"")
-    
-    path = path.replace(""chatapp-tutorial"", ""chatapp_tutorial"")
-    path = path.replace(""dashboard-tutorial"", ""dashboard_tutorial"")
-    
-    path = path.replace(""login-form"", ""login_form"")
-    path = path.replace(""signup-form"", ""signup_form"")
-    path = path.replace(""multi-column-row"", ""multi_column_row"")
-    path = path.replace(""top-banner"", ""top_banner"")
-    path = path.replace(""dark-mode-toggle"", ""dark_mode_toggle"")
-    path = path.replace(""pricing-cards"", ""pricing_cards"")
-    path = path.replace(""speed-dial"", ""speed_dial"")
-    
-    path = path.replace(""deploy-app"", ""deploy_app"")
-    path = path.replace(""download-app"", ""download_app"")
-    path = path.replace(""environment-variables"", ""environment_variables"")
-    path = path.replace(""image-as-prompt"", ""image_as_prompt"")
-    path = path.replace(""installing-external-packages"", ""installing_external_packages"")
-    path = path.replace(""frequently-asked-questions"", ""frequently_asked_questions"")
-    path = path.replace(""what-is-reflex-build"", ""what_is_reflex_build"")
-    path = path.replace(""breaking-up-complex-prompts"", ""breaking_up_complex_prompts"")
-    path = path.replace(""fixing-errors"", ""fixing_errors"")
-    
-    path = path.replace(""enterprise/ag-grid"", ""enterprise/ag_grid"")
-    path = path.replace(""ag-chart"", ""ag_chart"")
-    
-    path = path.replace(""page-load-events"", ""page_load_events"")
-    path = path.replace(""background-events"", ""background_events"")
-    path = path.replace(""yield-events"", ""yield_events"")
-    path = path.replace(""event-arguments"", ""event_arguments"")
-    path = path.replace(""event-actions"", ""event_actions"")
-    path = path.replace(""chaining-events"", ""chaining_events"")
-    path = path.replace(""special-events"", ""special_events"")
-    path = path.replace(""decentralized-event-handlers"", ""decentralized_event_handlers"")
-    path = path.replace(""events-overview"", ""events_overview"")
-    path = path.replace(""authentication-overview"", ""authentication_overview"")
-    path = path.replace(""dynamic-routing"", ""dynamic_routing"")
-    path = path.replace(""code-structure"", ""code_structure"")
-    path = path.replace(""component-state"", ""component_state"")
-    
-    path = path.replace(""segmented-control"", ""segmented_control"")
-    path = path.replace(""auto-scroll"", ""auto_scroll"")
-    path = path.replace(""code-block"", ""code_block"")
-    path = path.replace(""data-list"", ""data_list"")
-    path = path.replace(""scroll-area"", ""scroll_area"")
-    path = path.replace(""html-embed"", ""html_embed"")
-    path = path.replace(""aspect-ratio"", ""aspect_ratio"")
-    path = path.replace(""data-table"", ""data_table"")
-    path = path.replace(""data-editor"", ""data_editor"")
-    path = path.replace(""hover-card"", ""hover_card"")
-    path = path.replace(""alert-dialog"", ""alert_dialog"")
-    path = path.replace(""context-menu"", ""context_menu"")
-    path = path.replace(""dropdown-menu"", ""dropdown_menu"")
-    path = path.replace(""radio-group"", ""radio_group"")
-    path = path.replace(""text-area"", ""text_area"")
-    
-    path = path.replace(""custom-vars"", ""custom_vars"")
-    path = path.replace(""computed-vars"", ""computed_vars"")
-    path = path.replace(""base-vars"", ""base_vars"")
-    
-    path = path.replace(""config-file"", ""config_file"")
-    
-    path = path.replace(""upload-and-download-files"", ""upload_and_download_files"")
-    path = path.replace(""rendering-iterables"", ""rendering_iterables"")
-    path = path.replace(""html-to-reflex"", ""html_to_reflex"")
-    path = path.replace(""conditional-rendering"", ""conditional_rendering"")
-    path = path.replace(""other-methods"", ""other_methods"")
-    path = path.replace(""lifespan-tasks"", ""lifespan_tasks"")
-    path = path.replace(""exception-handlers"", ""exception_handlers"")
-    path = path.replace(""router-attributes"", ""router_attributes"")
-    path = path.replace(""event-triggers"", ""event_triggers"")
-    path = path.replace(""browser-storage"", ""browser_storage"")
-    path = path.replace(""var-system"", ""var_system"")
-    path = path.replace(""browser-javascript"", ""browser_javascript"")
+    if path.startswith(""docs/""):
+        path = path[5:]
+    
+    if path in url_to_filepath_map:
+        return url_to_filepath_map[path]
     
     if not path.endswith("".md""):
         path += "".md""
-    return path
+    return f""docs/{path}""
 
 def validate_edit_page_links():
     """"""Validate all edit page GitHub links return 200 OK.""""""