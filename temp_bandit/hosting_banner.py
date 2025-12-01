@@ -27,28 +27,33 @@ def hosting_banner() -> rx.Component:
             rx.link(
                 rx.box(
                     rx.box(
+                        # Header text with responsive spans
                         rx.text(
-                            ""Reflex Build - "",
+                            ""Reflex Build – "",
+                            # Descriptive text: hidden on small, inline on md+
                             rx.el.span(
                                 ""Build internal apps with AI."",
-                                # class_name=""text-slate-12 font-medium text-sm"",
                                 class_name=""hidden md:inline-block text-slate-12 font-medium text-sm"",
                             ),
-                            # ... keep this for mobile view if/when needed
+                            # Mobile CTA: inline on small, hidden on md+
                             rx.el.span(
                                 ""Try for Free!"",
-                                # class_name=""text-slate-12 font-medium text-sm"",
                                 class_name=""inline-block md:hidden text-slate-12 font-medium text-sm"",
                             ),
                             class_name=""text-slate-12 font-semibold text-sm z-[1]"",
                         ),
-                        # ... keep this for mobile view if/when needed
+                        # Standalone CTA button: hidden on small, inline on md+
                         rx.el.button(
                             ""Try for Free!"",
-                            class_name=""hidden md:inline-block text-green-11 h-[1.5rem] rounded-md bg-green-4 px-1.5 text-sm font-semibold z-[1] items-center justify-center shrink-0"",
+                            class_name=(
+                                ""hidden md:inline-block ""
+                                ""text-green-11 h-[1.5rem] rounded-md bg-green-4 ""
+                                ""px-1.5 text-sm font-semibold z-[1] items-center ""
+                                ""justify-center shrink-0""
+                            ),
                         ),
                         class_name=""flex items-center gap-4"",
-                    ),
+                    )
                 ),
                 glow(),
                 href=REFLEX_AI_BUILDER,