@@ -11,10 +11,7 @@
 
 @webpage(path=""/404"", title=""Page Not Found · Reflex.dev"", add_as_page=False)
 def page404():
-    return rx.center(
-        rx.vstack(
-            markdown_with_shiki(contents),
-            rx.spacer(),
-        ),
-        class_name=""h-[80vh] w-full"",
+    return rx.box(
+        markdown_with_shiki(contents),
+        class_name=""h-[80vh] w-full flex flex-col items-center justify-center"",
     )