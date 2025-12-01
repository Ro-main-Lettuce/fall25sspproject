@@ -91,7 +91,7 @@ def demo_section(color: str = ""slate"") -> rx.Component:
                         ""background"": ""linear-gradient(90deg, light-dark(rgba(249, 249, 251, 0.00), rgba(26, 27, 29, 0.00)) 0%, var(--c-slate-2) 79.62%)"",
                     },
                 ),
-                class_name=""desktop-only w-1/2 relative"",
+                class_name=""lg:flex hidden w-1/2 relative"",
             ),
             class_name=""flex flex-row w-full max-h-full h-[31rem] lg:h-[34rem] overflow-hidden"",
         ),