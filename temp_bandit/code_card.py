@@ -1,24 +1,42 @@
 import reflex as rx
+from reflex.experimental.client_state import ClientStateVar
+
+from pcweb.components.icons.hugeicons import hi
 from pcweb.components.icons.icons import get_icon
-from reflex.components.datadisplay.shiki_code_block import copy_script
 
 
+@rx.memo
 def install_command(
-    command: str, show_dollar_sign: bool = True, **props
+    command: str,
+    show_dollar_sign: bool = True,
 ) -> rx.Component:
+    copied = ClientStateVar.create(""is_copied"", default=False, global_ref=False)
     return rx.el.button(
-        rx.icon(""copy"", size=14, margin_left=""5px""),
+        rx.cond(
+            copied.value,
+            hi(
+                ""tick-02"",
+                size=14,
+                class_name=""ml-[5px] shrink-0"",
+            ),
+            hi(""copy-01"", size=14, class_name=""shrink-0 ml-[5px]""),
+        ),
         rx.text(
-            ""$"" + command if show_dollar_sign else command,
+            rx.cond(
+                show_dollar_sign,
+                f""${command}"",
+                command,
+            ),
             as_=""p"",
-            class_name=""flex-grow flex-shrink min-w-0 font-small text-start truncate"",
+            class_name=""font-small text-start truncate"",
         ),
         title=command,
         on_click=[
+            rx.call_function(copied.set_value(True)),
             rx.set_clipboard(command),
-            copy_script(),
         ],
-        class_name=""flex items-center gap-1.5 border-slate-5 bg-slate-1 hover:bg-slate-3 shadow-small pr-1.5 border rounded-md w-full max-w-full text-slate-9 transition-bg cursor-pointer overflow-hidden"",
+        on_mouse_down=rx.call_function(copied.set_value(False)).debounce(1500),
+        class_name=""flex items-center gap-1.5 border-slate-5 bg-slate-1 hover:bg-slate-3 shadow-small pr-1.5 border rounded-md w-full text-slate-9 transition-bg cursor-pointer overflow-hidden min-w-0 flex-1 h-[24px]"",
         style={
             ""opacity"": ""1"",
             ""cursor"": ""pointer"",
@@ -27,7 +45,6 @@ def install_command(
                 ""transition"": ""transform 0.250s ease-out, opacity 0.250s ease-out"",
             },
         },
-        **props,
     )
 
 
@@ -36,7 +53,7 @@ def repo(repo_url: str) -> rx.Component:
         get_icon(icon=""new_tab"", class_name=""p-[5px]""),
         href=repo_url,
         is_external=True,
-        class_name=""border-slate-5 bg-slate-1 hover:bg-slate-3 shadow-small border border-solid rounded-md text-slate-9 hover:!text-slate-9 no-underline transition-bg cursor-pointer"",
+        class_name=""border-slate-5 bg-slate-1 hover:bg-slate-3 shadow-small border border-solid rounded-md text-slate-9 hover:!text-slate-9 no-underline transition-bg cursor-pointer shrink-0"",
     )
 
 
@@ -48,12 +65,12 @@ def code_card(app: dict) -> rx.Component:
                     src=app[""image_url""],
                     loading=""lazy"",
                     alt=""Image preview for app: "" + app[""name""],
-                    class_name=""w-full h-full duration-150 object-top object-cover hover:scale-105 transition-transform ease-out"",
+                    class_name=""size-full duration-150 object-top object-cover hover:scale-105 transition-transform ease-out"",
                 ),
                 href=app[""demo_url""],
                 is_external=True,
             ),
-            class_name=""relative border-slate-5 border-b border-solid w-full h-full overflow-hidden"",
+            class_name=""relative border-slate-5 border-b border-solid w-full overflow-hidden h-[180px]"",
         ),
         rx.box(
             rx.box(
@@ -64,7 +81,9 @@ def code_card(app: dict) -> rx.Component:
                 class_name=""flex flex-row justify-between items-center gap-3 p-[0.625rem_0.75rem_0rem_0.75rem] w-full"",
             ),
             rx.box(
-                install_command(""reflex init --template "" + app[""demo_url""]),
+                install_command(
+                    ""reflex init --template "" + app[""demo_url""], show_dollar_sign=False
+                ),
                 rx.cond(app[""source""], repo(app[""source""])),
                 rx.link(
                     get_icon(icon=""eye"", class_name=""p-[5px]""),
@@ -87,87 +106,76 @@ def code_card(app: dict) -> rx.Component:
     )
 
 
-def gallery_app_card(app: dict) -> rx.Component:
+def gallery_app_card(app: dict[str, str]) -> rx.Component:
     return rx.flex(
         rx.box(
             rx.link(
                 rx.image(
                     src=app[""image""],
                     loading=""lazy"",
                     alt=""Image preview for app: "" + app[""title""],
-                    class_name=""w-full h-full duration-150 object-top object-cover hover:scale-105 transition-transform ease-out aspect-[1500/938]"",
+                    class_name=""size-full duration-150 object-cover hover:scale-105 transition-transform ease-out"",
                 ),
-                href=f""/templates/{app['title'].replace(' ', '-').lower()}"",
+                href=f""/docs/getting-started/open-source-templates/{app['title'].replace(' ', '-').lower()}"",
             ),
-            class_name=""relative border-slate-5 border-b border-solid w-full overflow-hidden h-[60%]"",
+            class_name=""relative border-slate-5 border-b border-solid w-full overflow-hidden h-[180px]"",
         ),
         rx.box(
             rx.box(
                 rx.el.h6(
                     app[""title""],
-                    class_name=""font-smbold text-slate-12 truncate"",
+                    class_name=""font-smbold text-slate-12 truncate shrink-0"",
                     width=""100%"",
                 ),
                 rx.text(
                     app[""description""],
-                    class_name=""text-slate-10 font-small truncate text-pretty"",
+                    class_name=""text-slate-10 font-small truncate text-pretty shrink-0"",
                     width=""100%"",
                 ),
                 rx.box(
-                    rx.vstack(
-                        rx.box(
-                            rx.hstack(
-                                install_command(
-                                    f""reflex init --template {app['title']}""
-                                ),
-                                *(
-                                    [
-                                        rx.hstack(
-                                            repo(app[""demo""]),
-                                            justify=""start"",
-                                        )
-                                    ]
-                                    if ""demo"" in app
-                                    else []
-                                ),
-                            ),
-                            width=""310px"",
-                            max_width=""310px"",
+                    rx.box(
+                        install_command(
+                            command=f""reflex init --template {app['title']}"",
+                            show_dollar_sign=False,
+                        ),
+                        *(
+                            [
+                                rx.box(
+                                    repo(app[""demo""]),
+                                    class_name=""flex flex-row justify-start"",
+                                )
+                            ]
+                            if ""demo"" in app
+                            else []
                         ),
-                        rx.cond(
-                            ""Reflex"" in app[""author""],
-                            rx.box(
-                                rx.text(
-                                    ""by"",
-                                    class_name=""text-slate-9 font-small"",
-                                ),
-                                get_icon(icon=""badge_logo""),
-                                rx.text(
-                                    app[""author""],
-                                    class_name=""text-slate-9 font-small"",
-                                ),
-                                class_name=""flex flex-row items-start gap-1"",
+                        class_name=""flex flex-row max-w-full gap-2 w-full shrink-0"",
+                    ),
+                    rx.box(class_name=""grow""),
+                    rx.cond(
+                        ""Reflex"" in app[""author""],
+                        rx.box(
+                            rx.text(
+                                ""by"",
+                                class_name=""text-slate-9 font-small"",
                             ),
+                            get_icon(icon=""badge_logo""),
                             rx.text(
-                                f""by {app['author']}"",
+                                app[""author""],
                                 class_name=""text-slate-9 font-small"",
                             ),
+                            class_name=""flex flex-row items-start gap-1"",
+                        ),
+                        rx.text(
+                            f""by {app['author']}"",
+                            class_name=""text-slate-9 font-small"",
                         ),
-                        align_items=""start"",
-                        class_name=""brother-john"",
                     ),
-                    class_name=""flex flex-row items-center gap-[6px] justify-between w-full"",
+                    class_name=""flex flex-col gap-[6px] size-full"",
                 ),
-                class_name=""flex flex-col justify-between items-start gap-1 p-[0.625rem_0.75rem_0.625rem_0.75rem] w-full h-full"",
+                class_name=""flex flex-col items-start gap-2 p-[0.625rem_0.75rem_0.625rem_0.75rem] w-full h-full"",
             ),
             class_name=""flex flex-col gap-[10px] w-full h-full flex-1"",
         ),
-        style={
-            ""animation"": ""fade-in 0.35s ease-out"",
-            ""@keyframes fade-in"": {
-                ""0%"": {""opacity"": ""0""},
-                ""100%"": {""opacity"": ""1""},
-            },
-        },
-        class_name=""box-border flex flex-col border-slate-5 bg-slate-1 shadow-large border rounded-xl w-full h-[320px] overflow-hidden"",
+        key=app[""title""],
+        class_name=""box-border flex-col border-slate-5 bg-slate-1 shadow-large border rounded-xl w-full h-[360px] overflow-hidden"",
     )