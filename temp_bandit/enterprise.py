@@ -5,13 +5,15 @@
 
 def get_sidebar_items_enterprise_usage():
     """"""Get the enterprise usage sidebar items.""""""
+    from pcweb.pages.docs import enterprise
+    
     return [
         SideBarItem(
             names=""Overview"",
             children=[
                 SideBarItem(
                     names=""How to use Enterprise"",
-                    link=""/docs/enterprise/overview/"",
+                    link=enterprise.overview.path,
                 ),
             ],
         ),
@@ -20,11 +22,11 @@ def get_sidebar_items_enterprise_usage():
             children=[
                 SideBarItem(
                     names=""Built with Reflex"",
-                    link=""/docs/enterprise/built-with-reflex/"",
+                    link=enterprise.built_with_reflex.path,
                 ),
                 SideBarItem(
                     names=""Single Port Proxy"",
-                    link=""/docs/enterprise/single-port-proxy/"",
+                    link=enterprise.single_port_proxy.path,
                 ),
             ],
         ),
@@ -33,41 +35,39 @@ def get_sidebar_items_enterprise_usage():
 
 def get_sidebar_items_enterprise_components():
     """"""Get the enterprise components sidebar items.""""""
+    from pcweb.pages.docs import enterprise
+    
     return [
         SideBarItem(
             names=""AG Grid"",
             children=[
                 SideBarItem(
                     names=""Overview"",
-                    link=""/docs/enterprise/ag_grid/"",
+                    link=enterprise.ag_grid.index.path,
                 ),
                 SideBarItem(
                     names=""Column Definitions"",
-                    link=""/docs/enterprise/ag_grid/column-defs/"",
+                    link=enterprise.ag_grid.column_defs.path,
                 ),
                 SideBarItem(
                     names=""Aligned Grids"",
-                    link=""/docs/enterprise/ag_grid/aligned-grids/"",
+                    link=enterprise.ag_grid.aligned_grids.path,
                 ),
                 SideBarItem(
                     names=""Model Wrapper"",
-                    link=""/docs/enterprise/ag_grid/model-wrapper/"",
+                    link=enterprise.ag_grid.model_wrapper.path,
                 ),
                 SideBarItem(
                     names=""Pivot Mode"",
-                    link=""/docs/enterprise/ag_grid/pivot-mode/"",
+                    link=enterprise.ag_grid.pivot_mode.path,
                 ),
                 SideBarItem(
                     names=""Theme"",
-                    link=""/docs/enterprise/ag_grid/theme/"",
+                    link=enterprise.ag_grid.theme.path,
                 ),
                 SideBarItem(
                     names=""Value Transformers"",
-                    link=""/docs/enterprise/ag_grid/value-transformers/"",
-                ),
-                SideBarItem(
-                    names=""Undocumented Features"",
-                    link=""/docs/enterprise/ag_grid/undocumented-features-guideline/"",
+                    link=enterprise.ag_grid.value_transformers.path,
                 ),
             ],
         ),
@@ -76,7 +76,7 @@ def get_sidebar_items_enterprise_components():
             children=[
                 SideBarItem(
                     names=""Overview"",
-                    link=""/docs/enterprise/ag_chart/"",
+                    link=enterprise.ag_chart.path,
                 ),
             ],
         ),
@@ -85,11 +85,11 @@ def get_sidebar_items_enterprise_components():
             children=[
                 SideBarItem(
                     names=""Drag and Drop"",
-                    link=""/docs/enterprise/drag-and-drop/"",
+                    link=enterprise.drag_and_drop.path,
                 ),
                 SideBarItem(
                     names=""Mapping"",
-                    link=""/docs/enterprise/map/"",
+                    link=enterprise.map.index.path,
                 ),
             ],
         ),
@@ -98,59 +98,59 @@ def get_sidebar_items_enterprise_components():
             children=[
                 SideBarItem(
                     names=""Overview"",
-                    link=""/docs/enterprise/mantine/"",
+                    link=enterprise.mantine.index.path,
                 ),
                 SideBarItem(
                     names=""Autocomplete"",
-                    link=""/docs/enterprise/mantine/autocomplete/"",
+                    link=enterprise.mantine.autocomplete.path,
                 ),
                 SideBarItem(
                     names=""Collapse"",
-                    link=""/docs/enterprise/mantine/collapse/"",
+                    link=enterprise.mantine.collapse.path,
                 ),
                 SideBarItem(
                     names=""JSON Input"",
-                    link=""/docs/enterprise/mantine/json-input/"",
+                    link=enterprise.mantine.json_input.path,
                 ),
                 SideBarItem(
                     names=""Loading Overlay"",
-                    link=""/docs/enterprise/mantine/loading-overlay/"",
+                    link=enterprise.mantine.loading_overlay.path,
                 ),
                 SideBarItem(
                     names=""Multi Select"",
-                    link=""/docs/enterprise/mantine/multi-select/"",
+                    link=enterprise.mantine.multi_select.path,
                 ),
                 SideBarItem(
                     names=""Number Formatter"",
-                    link=""/docs/enterprise/mantine/number-formatter/"",
+                    link=enterprise.mantine.number_formatter.path,
                 ),
                 SideBarItem(
                     names=""Pill"",
-                    link=""/docs/enterprise/mantine/pill/"",
+                    link=enterprise.mantine.pill.path,
                 ),
                 SideBarItem(
                     names=""Ring Progress"",
-                    link=""/docs/enterprise/mantine/ring-progress/"",
+                    link=enterprise.mantine.ring_progress.path,
                 ),
                 SideBarItem(
                     names=""Semi Circle Progress"",
-                    link=""/docs/enterprise/mantine/semi-circle-progress/"",
+                    link=enterprise.mantine.semi_circle_progress.path,
                 ),
                 SideBarItem(
                     names=""Spoiler"",
-                    link=""/docs/enterprise/mantine/spoiler/"",
+                    link=enterprise.mantine.spoiler.path,
                 ),
                 SideBarItem(
                     names=""Tags Input"",
-                    link=""/docs/enterprise/mantine/tags-input/"",
+                    link=enterprise.mantine.tags_input.path,
                 ),
                 SideBarItem(
                     names=""Timeline"",
-                    link=""/docs/enterprise/mantine/timeline/"",
+                    link=enterprise.mantine.timeline.path,
                 ),
                 SideBarItem(
                     names=""Tree"",
-                    link=""/docs/enterprise/mantine/tree/"",
+                    link=enterprise.mantine.tree.path,
                 ),
             ],
         ),