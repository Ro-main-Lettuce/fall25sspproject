@@ -22,13 +22,10 @@ class HubSample:
     """"""The images or image URLs associated with the sample""""""
 
     def _handle_image(self, image: str | Image.Image | Path) -> Image.Image:
-        if isinstance(image, Path):
-            return Image.open(image)
-        elif isinstance(image, str):
-            if image.startswith(""http""):
+        if isinstance(image, (Path, str)):
+            if isinstance(image, str) and image.startswith(""http""):
                 return remote_image(image)
-            else:
-                return Image.open(image)
+            return Image.open(image)
         elif isinstance(image, Image.Image):
             return image
         else: