@@ -6,12 +6,12 @@
 import pytest
 from playwright.sync_api import Page, expect
 
-import reflex as rx
 from reflex.testing import AppHarness
 
 
 def StatelessApp():
     """"""A stateless app that renders a heading.""""""
+    import reflex as rx
 
     def index():
         return rx.heading(""This is a stateless app"")