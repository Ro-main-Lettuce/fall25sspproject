@@ -19,7 +19,7 @@ def os_card() -> rx.Component:
             # Glow
             rx.html(
                 """"""<svg xmlns=""http://www.w3.org/2000/svg"" width=""300"" height=""89"" viewBox=""0 0 300 89"" fill=""none""><path d=""M300 44.5C300 69.077 232.978 89 150 89S0 69.077 0 44.5 67.022 0 150 0s150 19.923 150 44.5"" fill=""url(#a)""/><defs><radialGradient id=""a"" cx=""0"" cy=""0"" r=""1"" gradientUnits=""userSpaceOnUse"" gradientTransform=""scale(150 44.5)rotate(90 0 1)""><stop stop-color=""var(--c-violet-3)""/><stop offset=""1"" stop-color=""var(--c-slate-2)"" stop-opacity=""0""/></radialGradient></defs></svg>"""""",
-                class_name=""desktop-only shrink-0 absolute w-[18.75rem] h-[5.5625rem] -translate-y-1/2 left-[-3.5rem] top-1/2"",
+                class_name=""lg:flex hidden shrink-0 absolute w-[18.75rem] h-[5.5625rem] -translate-y-1/2 left-[-3.5rem] top-1/2"",
             ),
             button(
                 ""Contribute on GitHub"",
@@ -29,7 +29,7 @@ def os_card() -> rx.Component:
             href=GITHUB_URL,
             class_name=""relative w-full lg:w-auto"",
         ),
-        class_name=""flex flex-col gap-8 w-full p-10 pb-12 lg:!border-l !border-slate-3 lg:!border-t items-center lg:items-start text-center lg:text-start"",
+        class_name=""lg:!border-b-0 flex flex-col gap-8 w-full p-10 pb-12 lg:!border-l !border-slate-3 items-center lg:items-start text-center lg:text-start"",
     )
 
 
@@ -71,7 +71,7 @@ def newletter_input() -> rx.Component:
     </radialGradient>
   </defs>
 </svg>"""""",
-                        class_name=""desktop-only shrink-0 absolute -translate-y-1/2 left-[-2.5rem] top-1/2 h-[5.5625rem] w-[25.1875rem] z-[-1]"",
+                        class_name=""lg:flex hidden shrink-0 absolute -translate-y-1/2 left-[-2.5rem] top-1/2 h-[5.5625rem] w-[25.1875rem] z-[-1]"",
                     ),
                     rx.el.input(
                         placeholder=""Your email"",
@@ -93,7 +93,7 @@ def newletter_input() -> rx.Component:
     </radialGradient>
   </defs>
 </svg>"""""",
-                        class_name=""desktop-only shrink-0 absolute w-[11.4375rem] h-[5.5625rem] -translate-y-1/2 right-[-2.5rem] top-1/2 z-[-1]"",
+                        class_name=""lg:flex hidden shrink-0 absolute w-[11.4375rem] h-[5.5625rem] -translate-y-1/2 right-[-2.5rem] top-1/2 z-[-1]"",
                     ),
                     button(
                         ""Subscribe"",