@@ -6,7 +6,7 @@
 def get_component_link(category, clist, prefix="""") -> str:
     component_name = rx.utils.format.to_kebab_case(clist[0])
     # construct the component link. The component name points to the name of the md file.
-    return f""/docs/library/{prefix.strip('/')}/{category.lower().replace(' ', '-')}/{component_name.lower()}""
+    return f""/docs/library/{prefix.strip('/') + '/' if prefix.strip('/') else ''}{category.lower().replace(' ', '-')}/{component_name.lower()}""
 
 
 def get_category_children(category, category_list, prefix=""""):
@@ -22,7 +22,7 @@ def get_category_children(category, category_list, prefix=""""):
     category_item_children.append(
         SideBarItem(
             names=""Overview"",
-            link=f""/docs/library/{prefix}{category.lower().replace(' ', '-')}/"",
+            link=f""/docs/library/{prefix if prefix else ''}{category.lower().replace(' ', '-')}/"",
         )
     )
     for c in category_list: