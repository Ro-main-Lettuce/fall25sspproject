@@ -30,6 +30,7 @@
 
 from pcweb.pages.framework.views.footer_index import dark_mode_toggle
 
+
 def footer_link(text: str, href: str) -> rx.Component:
     return rx.link(
         text,