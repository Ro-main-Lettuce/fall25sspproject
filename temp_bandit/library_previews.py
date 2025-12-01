@@ -72,7 +72,7 @@ def page() -> rx.Component:
                     component_card(
                         name=component[0],
                         link=get_component_link(
-                            component_category, component, prefix.strip(""/"") + ""/""
+                            component_category, component, prefix.strip(""/"") + ""/"" if prefix.strip(""/"") else """"
                         ),
                         section=component_category,
                     )