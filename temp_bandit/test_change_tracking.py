@@ -22,7 +22,7 @@ def test_change_tracking_format(self, mock_post):
         }
         mock_post.return_value = mock_response
 
-        app = FirecrawlApp(api_key=os.environ.get('FIRECRAWL_API_KEY', 'dummy-api-key-for-testing'))
+        app = FirecrawlApp(api_key=os.environ.get('TEST_API_KEY', 'dummy-api-key-for-testing'))
         result = app.scrape_url('https://example.com', {
             'formats': ['markdown', 'changeTracking']
         })
@@ -80,7 +80,7 @@ def test_change_tracking_options(self, mock_post):
         }
         mock_post.return_value = mock_response
 
-        app = FirecrawlApp(api_key=os.environ.get('FIRECRAWL_API_KEY', 'dummy-api-key-for-testing'))
+        app = FirecrawlApp(api_key=os.environ.get('TEST_API_KEY', 'dummy-api-key-for-testing'))
         result = app.scrape_url('https://example.com', {
             'formats': ['markdown', 'changeTracking'],
             'changeTrackingOptions': {