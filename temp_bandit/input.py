@@ -898,7 +898,10 @@ class dropdown(UIElement[List[str], Any]):
 
         # With search functionality
         dropdown = mo.ui.dropdown(
-            options=[""a"", ""b"", ""c""], value=""a"", label=""choose one"", searchable=True
+            options=[""a"", ""b"", ""c""],
+            value=""a"",
+            label=""choose one"",
+            searchable=True,
         )
         ```
 