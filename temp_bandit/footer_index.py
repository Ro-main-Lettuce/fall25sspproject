@@ -49,7 +49,7 @@ def footer_link(text: str, href: str) -> rx.Component:
         rx.icon(
             tag=""chevron-right"",
             size=16,
-            class_name=""shrink-0 mobile-only"",
+            class_name=""shrink-0 lg:hidden flex"",
         ),
         href=href,
         class_name=""font-small text-slate-9 hover:!text-slate-11 no-underline transition-color w-full lg:w-fit flex flex-row justify-between items-center"",
@@ -143,7 +143,7 @@ def newsletter() -> rx.Component:
                 class_name=""font-small text-slate-9"",
             ),
             newletter_input(),
-            class_name=""flex flex-col items-center lg:items-start gap-4 self-stretch p-10"",
+            class_name=""flex flex-col items-center lg:items-start gap-4 self-stretch p-10 lg:border-r border-slate-3"",
         ),
     )
 
@@ -195,7 +195,7 @@ def footer_index() -> rx.Component:
                     class_name=""font-small text-slate-9"",
                 ),
                 menu_socials(),
-                class_name=""flex flex-col items-center lg:items-start gap-4 self-stretch p-10"",
+                class_name=""flex flex-col items-center lg:items-start gap-4 self-stretch p-10 lg:border-l border-slate-3"",
             ),
             newsletter(),
             class_name=""grid grid-cols-1 lg:grid-cols-3 gap-0 grid-rows-2 w-full divide-y divide-slate-3 lg:divide-x border-t border-slate-3 lg:border-t-0"",