@@ -3,7 +3,7 @@
 import itertools
 from typing import TYPE_CHECKING
 
-from pcweb.telemetry import pixels_google, pixels_koala, pixels_rb2b, pixels_posthog
+from pcweb.telemetry import pixels_google, pixels_signals, pixels_rb2b, pixels_posthog
 
 if TYPE_CHECKING:
     import reflex as rx
@@ -13,7 +13,7 @@ def get_pixel_website_trackers() -> list[rx.Component]:
     return list(
         itertools.chain(
             pixels_google.get_pixel_website_trackers(),
-            pixels_koala.get_pixel_website_trackers(),
+            pixels_signals.get_pixel_website_trackers(),
             pixels_rb2b.get_pixel_rb2b_website_trackers(),
             pixels_posthog.get_pixel_website_trackers(),
         ),