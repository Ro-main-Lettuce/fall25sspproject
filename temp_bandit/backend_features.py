@@ -113,7 +113,7 @@ def pip_install_card() -> rx.Component:
             on_click=rx.set_clipboard(""pip install reflex""),
             class_name=""flex flex-row items-center gap-1.5 px-1.5 py-1 rounded-lg cursor-pointer transition-bg border border-solid border-slate-4 bg-[rgba(249,249,251,0.48)] dark:bg-[rgba(26,27,29,0.48)] hover:bg-[rgba(249,249,251,0.48)] dark:hover:bg-[rgba(26,27,29,0.48)] backdrop-filter backdrop-blur-[6px]"",
         ),
-        class_name=""desktop-only h-full w-full justify-center items-center relative overflow-hidden row-span-2 lg:!border-r !border-slate-3 !border-t-0"",
+        class_name=""lg:flex hidden h-full w-full justify-center items-center relative overflow-hidden row-span-2 lg:!border-r !border-slate-3 !border-t-0"",
     )
 
 
@@ -158,6 +158,7 @@ def backend_grid() -> rx.Component:
             title=""It's just Python"",
             description=""Define and manage state with Python classes and functions"",
             icon=""python"",
+            class_name=""lg:!border-l !border-slate-3"",
         ),
         backend_card(
             title=""PyPI"",
@@ -168,11 +169,13 @@ def backend_grid() -> rx.Component:
             title=""Database management"",
             description=""Use our built-in database or connect your own with a single line"",
             icon=""backend_db"",
+            class_name=""lg:!border-l lg:!border-b-0 !border-slate-3"",
         ),
         backend_card(
             title=""Auth"",
             description=""Secure your app with any auth provider - no vendor lock-in"",
             icon=""backend_auth"",
+            class_name=""lg:!border-b-0"",
         ),
         backend_card(
             title=""Check out the docs"",