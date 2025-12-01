@@ -6,9 +6,11 @@
 
 document = flexdown.parse_file(""pcweb/pages/databricks/databricks.md"")
 
+
 def databricks_content() -> rx.Component:
     return rx.box(xd.render(document, document.filename))
 
+
 @highlight_page(path=""/databricks"", title=""Databricks - Reflex"")
 def databricks_page():
     return databricks_content()