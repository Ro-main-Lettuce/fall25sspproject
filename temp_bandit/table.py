@@ -306,7 +306,7 @@ def create_feature_table_header(section: str, badge: str = None) -> rx.Component
 def table_body_oss() -> rx.Component:
     return rx.table.root(
         rx.table.header(
-            create_feature_table_header(""Reflex Build"", badge=""Early Access""),
+            create_feature_table_header(""Reflex Build""),
             class_name=""relative"",
         ),
         create_table_body(