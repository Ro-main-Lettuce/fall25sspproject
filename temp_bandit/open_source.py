@@ -3,8 +3,6 @@
 from pcweb.constants import GITHUB_STARS, CONTRIBUTION_URL, BUGS_URL
 
 
-
-
 def stat(icon: str, stat: str, text: str) -> rx.Component:
     return rx.box(
         get_icon(icon),