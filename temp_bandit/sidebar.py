@@ -381,7 +381,8 @@ def sidebar_comp(
     graphing_libs_index: list[int],
     api_reference_index: list[int],
     recipes_index: list[int],
-    enterprise_index: list[int],
+    enterprise_usage_index: list[int],
+    enterprise_component_index: list[int],
     #
     cli_ref_index: list[int],
     ai_builder_overview_index: list[int],
@@ -597,14 +598,14 @@ def sidebar_comp(
                                     ""Enterprise Usage"",
                                     enterprise.overview.path,
                                     enterprise_usage_items,
-                                    enterprise_index,
+                                    enterprise_usage_index,
                                     url,
                                 ),
                                 create_sidebar_section(
                                     ""Components"",
                                     enterprise.components.path,
                                     enterprise_component_items,
-                                    enterprise_index,
+                                    enterprise_component_index,
                                     url,
                                 ),
                                 class_name=""flex flex-col items-start gap-6 p-[0px_1rem_0px_0.5rem] w-full list-none list-style-none"",
@@ -637,7 +638,8 @@ def sidebar(url=None, width: str = ""100%"") -> rx.Component:
     graphing_libs_index = calculate_index(graphing_libs, url)
     api_reference_index = calculate_index(api_reference, url)
     recipes_index = calculate_index(recipes, url)
-    enterprise_index = calculate_index(enterprise_items, url)
+    enterprise_usage_index = calculate_index(enterprise_usage_items, url)
+    enterprise_component_index = calculate_index(enterprise_component_items, url)
 
     cli_ref_index = calculate_index(cli_ref, url)
     ai_builder_overview_index = calculate_index(ai_builder_overview_items, url)
@@ -653,7 +655,8 @@ def sidebar(url=None, width: str = ""100%"") -> rx.Component:
             graphing_libs_index=graphing_libs_index,
             api_reference_index=api_reference_index,
             recipes_index=recipes_index,
-            enterprise_index=enterprise_index,
+            enterprise_usage_index=enterprise_usage_index,
+            enterprise_component_index=enterprise_component_index,
             ai_builder_overview_index=ai_builder_overview_index,
             cli_ref_index=cli_ref_index,
             #