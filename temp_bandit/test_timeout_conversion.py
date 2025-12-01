@@ -25,7 +25,7 @@ def test_scrape_url_timeout_conversion(self, mock_post):
         self.assertEqual(kwargs['timeout'], 65.0)
 
     @patch('requests.post')
-    def test_scrape_url_no_timeout(self, mock_post):
+    def test_scrape_url_default_timeout(self, mock_post):
         mock_response = MagicMock()
         mock_response.status_code = 200
         mock_response.json.return_value = {
@@ -40,7 +40,7 @@ def test_scrape_url_no_timeout(self, mock_post):
         app.scrape_url('https://example.com')
 
         args, kwargs = mock_post.call_args
-        self.assertIsNone(kwargs['timeout'])
+        self.assertEqual(kwargs['timeout'], 35.0)
 
     @patch('requests.post')
     def test_post_request_timeout_conversion(self, mock_post):
@@ -59,20 +59,20 @@ def test_post_request_timeout_conversion(self, mock_post):
         self.assertEqual(kwargs['timeout'], 35.0)
 
     @patch('requests.post')
-    def test_post_request_no_timeout(self, mock_post):
+    def test_post_request_default_timeout(self, mock_post):
         mock_response = MagicMock()
         mock_response.status_code = 200
         mock_post.return_value = mock_response
 
         app = FirecrawlApp(api_key=os.environ.get('TEST_API_KEY', 'dummy-api-key-for-testing'))
         
-        data = {'url': 'https://example.com'}
+        data = {'timeout': 30000, 'url': 'https://example.com'}
         headers = {'Content-Type': 'application/json'}
         
         app._post_request('https://example.com/api', data, headers)
 
         args, kwargs = mock_post.call_args
-        self.assertIsNone(kwargs['timeout'])
+        self.assertEqual(kwargs['timeout'], 35.0)
 
     @patch('requests.post')
     def test_timeout_edge_cases(self, mock_post):
@@ -96,6 +96,22 @@ def test_timeout_edge_cases(self, mock_post):
         args, kwargs = mock_post.call_args
         self.assertEqual(kwargs['timeout'], 5.0)
 
+    @patch('requests.post')
+    def test_post_request_no_timeout_key(self, mock_post):
+        mock_response = MagicMock()
+        mock_response.status_code = 200
+        mock_post.return_value = mock_response
+
+        app = FirecrawlApp(api_key=os.environ.get('TEST_API_KEY', 'dummy-api-key-for-testing'))
+        
+        data = {'url': 'https://example.com'}
+        headers = {'Content-Type': 'application/json'}
+        
+        app._post_request('https://example.com/api', data, headers)
+
+        args, kwargs = mock_post.call_args
+        self.assertIsNone(kwargs['timeout'])
+
 
 if __name__ == '__main__':
     unittest.main()