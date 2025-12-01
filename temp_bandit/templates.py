@@ -1,4 +1,5 @@
 import reflex as rx
+import copy
 
 
 def gallery_app_card(app: dict) -> rx.Component:
@@ -49,8 +50,10 @@ def gallery_app_card(app: dict) -> rx.Component:
 def component_grid() -> rx.Component:
     from pcweb.pages.gallery.apps import gallery_apps_data
 
+    apps_copy = copy.deepcopy(gallery_apps_data)
+
     posts = []
-    for path, document in list(gallery_apps_data.items()):
+    for path, document in list(apps_copy.items()):
         document.metadata[""url""] = document.metadata[""title""]
         document.metadata[""title""] = templates_name_map.get(
             document.metadata[""title""], document.metadata[""title""]