@@ -71,6 +71,35 @@ def test_get_ssl_verify_config_fallback_to_certifi(self):
                 result = get_ssl_verify_config()
                 assert result == '/path/to/certifi/cacert.pem'
 
+    def test_get_ssl_verify_config_file_format_validation(self):
+        """"""Test that CA bundle file format validation works correctly.""""""
+        with tempfile.NamedTemporaryFile(suffix="".pem"", delete=False) as temp_file:
+            temp_path = temp_file.name
+        
+        try:
+            with patch.dict(os.environ, {""REQUESTS_CA_BUNDLE"": temp_path}):
+                result = get_ssl_verify_config()
+                assert result == temp_path
+        finally:
+            os.unlink(temp_path)
+
+    def test_get_ssl_verify_config_unsupported_format_warning(self):
+        """"""Test that unsupported file formats still work but show warning.""""""
+        with tempfile.NamedTemporaryFile(suffix="".txt"", delete=False) as temp_file:
+            temp_path = temp_file.name
+        
+        try:
+            with patch.dict(os.environ, {""REQUESTS_CA_BUNDLE"": temp_path}):
+                with patch('click.secho') as mock_secho:
+                    result = get_ssl_verify_config()
+                    assert result == temp_path
+                    mock_secho.assert_called_with(
+                        f""Warning: CA bundle file {temp_path} may not be in expected format (.pem, .crt, .cer)"", 
+                        fg=""yellow""
+                    )
+        finally:
+            os.unlink(temp_path)
+
 
 class TestFetchProviderDataSSL:
     def test_fetch_provider_data_uses_ssl_config(self):
@@ -99,7 +128,8 @@ def test_fetch_provider_data_ssl_error_handling(self):
                 
                 assert result is None
                 mock_secho.assert_any_call(""SSL certificate verification failed: SSL verification failed"", fg=""red"")
-                mock_secho.assert_any_call(""Try setting REQUESTS_CA_BUNDLE environment variable to your CA bundle path"", fg=""yellow"")
+                mock_secho.assert_any_call(""Solutions:"", fg=""cyan"")
+                mock_secho.assert_any_call(""  1. Set REQUESTS_CA_BUNDLE environment variable to your CA bundle path"", fg=""yellow"")
 
     def test_fetch_provider_data_general_request_error(self):
         cache_file = Path(""/tmp/test_cache.json"")