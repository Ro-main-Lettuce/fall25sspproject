@@ -12,7 +12,7 @@
     ""apple"",
     ""microsoft"",
     ""amazon"",
-    ""fastly"",    
+    ""fastly"",
     ""accenture"",
     ""ibm"",
     ""unicef"",
@@ -95,7 +95,7 @@ def quote_box(company: str) -> rx.Component:
     case_study = companies_case_studies_var[company]
     return rx.fragment(
         rx.text(
-            f'“{case_study[""quote""]}”',
+            f""“{case_study['quote']}”"",
             class_name=""text-xs text-slate-12 italic font-medium animate-fade animate-duration-[750ms] animate-fill-both"",
         ),
         rx.box(