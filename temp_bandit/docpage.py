@@ -270,7 +270,7 @@ def link_pill(text: str, href: str) -> rx.Component:
         text,
         href=href,
         underline=""none"",
-        class_name=""desktop-only flex flex-row justify-center items-center gap-2 lg:border-slate-5 bg-slate-3 lg:bg-slate-1 hover:bg-slate-3 shadow-none lg:shadow-large px-3 py-0.5 lg:border lg:border-solid border-none rounded-lg lg:rounded-full w-auto font-small font-small text-slate-9 !hover:text-slate-11 hover:!text-slate-9 truncate whitespace-nowrap transition-bg transition-color cursor-pointer"",
+        class_name=""lg:flex hidden flex-row justify-center items-center gap-2 lg:border-slate-5 bg-slate-3 lg:bg-slate-1 hover:bg-slate-3 shadow-none lg:shadow-large px-3 py-0.5 lg:border lg:border-solid border-none rounded-lg lg:rounded-full w-auto font-small font-small text-slate-9 !hover:text-slate-11 hover:!text-slate-9 truncate whitespace-nowrap transition-bg transition-color cursor-pointer"",
     )
 
 
@@ -305,7 +305,7 @@ def docpage_footer(path: str):
                     ""Edit this page"",
                     f""https://github.com/reflex-dev/reflex-web/tree/main{path}.md"",
                 ),
-                class_name=""desktop-only flex-row items-center gap-2 w-auto"",
+                class_name=""lg:flex hidden flex-row items-center gap-2 w-auto"",
             ),
             class_name=""flex flex-row justify-center lg:justify-between items-center border-slate-4 border-y-0 lg:border-y pt-0 lg:pt-8 pb-6 lg:pb-8 w-full"",
         ),
@@ -397,13 +397,13 @@ def breadcrumb(path: str, nav_sidebar: rx.Component):
                 rx.icon(
                     tag=""chevron-right"",
                     size=14,
-                    class_name=""desktop-only !text-slate-8"",
+                    class_name=""lg:flex hidden !text-slate-8"",
                 ),
             )
             breadcrumbs.append(
                 rx.text(
                     ""/"",
-                    class_name=""font-sm text-slate-8 mobile-only"",
+                    class_name=""font-sm text-slate-8 lg:hidden flex"",
                 )
             )
     from pcweb.components.hosting_banner import HostingBannerState
@@ -413,7 +413,7 @@ def breadcrumb(path: str, nav_sidebar: rx.Component):
         docs_sidebar_drawer(
             nav_sidebar,
             trigger=rx.box(
-                class_name=""absolute inset-0 bg-transparent z-[1] mobile-only"",
+                class_name=""absolute inset-0 bg-transparent z-[1] lg:hidden flex"",
             ),
         ),
         rx.box(
@@ -422,7 +422,7 @@ def breadcrumb(path: str, nav_sidebar: rx.Component):
         ),
         rx.box(
             rx.icon(tag=""chevron-down"", size=14, class_name=""!text-slate-9""),
-            class_name=""p-[0.563rem] mobile-only"",
+            class_name=""p-[0.563rem] lg:hidden flex"",
         ),
         class_name=""relative z-10 flex flex-row justify-between items-center gap-4 lg:gap-0 border-slate-4 bg-slate-1 mt-12 mb-6 lg:mb-12 p-[0.5rem_1rem_0.5rem_1rem] lg:p-0 border-b lg:border-none w-full""
         + rx.cond(
@@ -625,7 +625,7 @@ def wrapper(*args, **kwargs) -> rx.Component:
                 rx.el.main(
                     rx.box(
                         sidebar,
-                        class_name=""h-full shrink-0 desktop-only lg:block hidden""
+                        class_name=""h-full shrink-0 lg:block hidden""
                         + rx.cond(
                             HostingBannerState.show_banner,
                             "" mt-[146px]"",
@@ -635,7 +635,8 @@ def wrapper(*args, **kwargs) -> rx.Component:
                     rx.box(
                         rx.box(
                             breadcrumb(path=path, nav_sidebar=nav_sidebar),
-                            class_name=""px-0 xl:px-20 pt-0 "" + rx.cond(
+                            class_name=""px-0 xl:px-20 pt-0 ""
+                            + rx.cond(
                                 HostingBannerState.show_banner,
                                 ""mt-[90px]"",
                                 """",