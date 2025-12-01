@@ -1,9 +1,9 @@
 """"""Search bar component for the navbar.""""""
 
 import reflex as rx
-from .inkeep import inkeep
+from .typesense import typesense_search
 
 
 @rx.memo
 def search_bar() -> rx.Component:
-    return inkeep()
+    return typesense_search()