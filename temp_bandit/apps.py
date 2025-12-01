@@ -7,7 +7,7 @@
 from pcweb.pages.gallery import gallery
 from pcweb.components.button import button, button_with_icon
 from pcweb.components.code_card import gallery_app_card
-
+import copy
 
 GALLERY_APPS_PATH = ""templates/""
 
@@ -28,12 +28,12 @@ def get_route(path: str):
 
 paths = flexdown.utils.get_flexdown_files(GALLERY_APPS_PATH)
 gallery_apps_data = get_gallery_apps(paths)
-gallery_apps_data_copy = gallery_apps_data.copy()
 
 
 def more_posts(current_post: dict) -> rx.Component:
     posts = []
-    app_items = list(gallery_apps_data_copy.items())
+    app_copy = copy.deepcopy(gallery_apps_data)
+    app_items = list(app_copy.items())
     current_index = next(
         (
             i