@@ -1,5 +1,4 @@
 import reflex as rx
-from tailwind_config import tw_config
 
 config = rx.Config(
     port=3000,
@@ -11,5 +10,5 @@
     ],
     show_build_with_reflex=False,
     telemetry_enabled=False,
-    plugins=[rx.plugins.TailwindV3Plugin(tw_config), rx.plugins.SitemapPlugin()],
+    plugins=[rx.plugins.TailwindV4Plugin(), rx.plugins.SitemapPlugin()],
 )