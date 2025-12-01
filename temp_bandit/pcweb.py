@@ -4,13 +4,14 @@
 import sys
 
 import reflex as rx
+
 import reflex_enterprise as rxe
 from pcweb import styles
+from pcweb.meta.meta import favicons_links
 from pcweb.pages import page404, routes
-from pcweb.pages.docs import outblocks, exec_blocks
-from pcweb.whitelist import _check_whitelisted_path
+from pcweb.pages.docs import exec_blocks, outblocks
 from pcweb.telemetry import get_pixel_website_trackers
-from pcweb.meta.meta import favicons_links
+from pcweb.whitelist import _check_whitelisted_path
 
 # This number discovered by trial and error on Windows 11 w/ Node 18, any
 # higher and the prod build fails with EMFILE error.