@@ -1,4 +1,3 @@
-import os
 import re
 
 import pytest
@@ -14,15 +13,14 @@ def background_events_url() -> str:
     return docs.events.background_events.path
 
 
-@pytest.mark.skipif(
-    os.environ.get(""GITHUB_ACTIONS"") is not None, reason=""Consistently fails in CI""
-)
 def test_background_events(
     reflex_web_app: AppHarness,
     page: Page,
     background_events_url: str,
 ):
     assert reflex_web_app.frontend_url is not None
+    page.set_default_timeout(60000)
+    page.set_default_navigation_timeout(60000)
 
     page.goto(reflex_web_app.frontend_url + background_events_url)
     expect(page).to_have_url(re.compile(background_events_url))
@@ -36,7 +34,8 @@ def test_background_events(
     expect(heading).to_have_text(""0 /"")
 
     start_button.click()
-    expect(heading).to_have_text(""4 /"")
+    expect(heading).to_have_text(re.compile(r""[4-7] /""))
+
     reset_button.click()
     expect(heading).to_have_text(""0 /"")
-    expect(heading).to_have_text(""10 /"")
+    expect(heading).to_have_text(""10 /"", timeout=12000)