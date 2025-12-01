@@ -18,7 +18,7 @@ def h_comp_common(
     class_name: str = """",
 ) -> rx.Component:
     id_ = text.lower().split("" "").join(""-"")
-    href = rx.State.router.page.full_path + ""#"" + id_
+    href = rx.State.router.url + ""#"" + id_
 
     return rx.link(
         rx.heading(