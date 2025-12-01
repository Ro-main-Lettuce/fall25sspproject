@@ -76,14 +76,11 @@ def test_deploy_url(deploy_url_sample: AppHarness, driver: WebDriver) -> None:
         deploy_url_sample: AppHarness fixture for testing deploy_url.
         driver: WebDriver fixture for testing deploy_url.
     """"""
-    import reflex as rx
-
-    deploy_url = rx.config.get_config().deploy_url
-    assert deploy_url is not None
-    assert deploy_url != ""http://localhost:3000""
-    assert deploy_url == deploy_url_sample.frontend_url
-    driver.get(deploy_url)
-    assert driver.current_url.removesuffix(""/"") == deploy_url.removesuffix(""/"")
+    assert deploy_url_sample.frontend_url is not None
+    assert (
+        deploy_url_sample.frontend_url
+        in (deploy_url_sample.app_path / "".web"" / ""public"" / ""sitemap.xml"").read_text()
+    )
 
 
 def test_deploy_url_in_app(deploy_url_sample: AppHarness, driver: WebDriver) -> None: