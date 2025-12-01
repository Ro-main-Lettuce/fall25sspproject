@@ -2,6 +2,7 @@
 from pcweb.components.icons.hugeicons import hi
 from pcweb.pages.framework.demos.demos import demo_section
 
+
 def header() -> rx.Component:
     return rx.box(
         rx.image(
@@ -30,6 +31,6 @@ def header() -> rx.Component:
 def framework_section() -> rx.Component:
     return rx.el.section(
         header(),
-        demo_section(color=""jade""), 
+        demo_section(color=""jade""),
         class_name=""flex flex-col mx-auto w-full max-w-[84.19rem] justify-center items-center"",
     )