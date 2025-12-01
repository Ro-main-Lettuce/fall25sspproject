@@ -74,7 +74,7 @@ def card(company: str, text: str, class_name: str = """") -> rx.Component:
                 tag=""chevron-right"",
                 class_name=""!text-slate-9 size-3.5 group-hover:translate-x-0.5 transition-transform duration-150"",
             ),
-            class_name=""absolute bottom-10 right-10 items-center gap-2 desktop-only"",
+            class_name=""absolute bottom-10 right-10 items-center gap-2 lg:flex hidden"",
         ),
         href=f""/customers/{company.lower()}"",
         class_name=""rounded-[1.125rem] border border-solid border-slate-4 bg-slate-2 p-10 overflow-hidden relative h-[23.25rem] lg:shadow-large group""