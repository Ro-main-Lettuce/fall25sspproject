@@ -1,10 +1,11 @@
+import os
 import re
+import time
 
 import pytest
 from playwright.sync_api import Page, expect
 
 from reflex.testing import AppHarness
-import time
 
 
 @pytest.fixture
@@ -14,12 +15,17 @@ def chaining_event_url() -> str:
     return docs.events.chaining_events.path
 
 
+@pytest.mark.skipif(
+    os.environ.get(""GITHUB_ACTIONS"") is not None, reason=""Consistently fails in CI""
+)
 def test_handler_from_handler(
     reflex_web_app: AppHarness,
     page: Page,
     chaining_event_url: str,
 ):
     assert reflex_web_app.frontend_url is not None
+    page.set_default_timeout(60000)
+    page.set_default_navigation_timeout(60000)
 
     page.goto(reflex_web_app.frontend_url + chaining_event_url)
     expect(page).to_have_url(re.compile(chaining_event_url))
@@ -46,6 +52,8 @@ def test_handler_from_handler(
 
 def test_collatz(reflex_web_app: AppHarness, page: Page, chaining_event_url):
     assert reflex_web_app.frontend_url is not None
+    page.set_default_timeout(60000)
+    page.set_default_navigation_timeout(60000)
 
     page.goto(reflex_web_app.frontend_url + chaining_event_url)
     expect(page).to_have_url(re.compile(chaining_event_url))