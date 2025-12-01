@@ -22,7 +22,7 @@ def generate_gallery(
                             class_name=""font-large text-slate-12"",
                         ),
                         get_icon(""new_tab"", class_name=""text-slate-11 [&>svg]:size-4""),
-                        href=f""/docs/library/{prefix.strip('/')}/{category.lower()}"",
+                        href=f""/docs/library/{prefix.strip('/') + '/' if prefix.strip('/') else ''}{category.lower()}"",
                         underline=""none"",
                         class_name=""px-4 py-2 bg-slate-1 hover:bg-slate-3 transition-bg flex flex-row justify-between items-center !text-slate-12"",
                     ),