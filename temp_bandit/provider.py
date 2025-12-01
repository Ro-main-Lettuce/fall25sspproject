@@ -170,11 +170,22 @@ def get_ssl_verify_config():
     Example:
         >>> get_ssl_verify_config()
         '/path/to/ca-bundle.pem'
+        
+        >>> os.environ['REQUESTS_CA_BUNDLE'] = '/custom/ca-bundle.pem'
+        >>> get_ssl_verify_config()
+        '/custom/ca-bundle.pem'
     """"""
     for env_var in ['REQUESTS_CA_BUNDLE', 'SSL_CERT_FILE', 'CURL_CA_BUNDLE']:
         ca_bundle = os.environ.get(env_var)
-        if ca_bundle and os.path.isfile(ca_bundle):
-            return ca_bundle
+        if ca_bundle:
+            ca_path = Path(ca_bundle)
+            if ca_path.is_file() and ca_path.suffix in ['.pem', '.crt', '.cer']:
+                return str(ca_path)
+            elif ca_path.is_file():
+                click.secho(f""Warning: CA bundle file {ca_bundle} may not be in expected format (.pem, .crt, .cer)"", fg=""yellow"")
+                return str(ca_path)
+            else:
+                click.secho(f""Warning: CA bundle path {ca_bundle} from {env_var} does not exist"", fg=""yellow"")
     
     return certifi.where()
 
@@ -200,7 +211,10 @@ def fetch_provider_data(cache_file):
     except requests.exceptions.SSLError as e:
         click.secho(f""SSL certificate verification failed: {e}"", fg=""red"")
         click.secho(f""Current CA bundle path: {ssl_config}"", fg=""yellow"")
-        click.secho(""Try setting REQUESTS_CA_BUNDLE environment variable to your CA bundle path"", fg=""yellow"")
+        click.secho(""Solutions:"", fg=""cyan"")
+        click.secho(""  1. Set REQUESTS_CA_BUNDLE environment variable to your CA bundle path"", fg=""yellow"")
+        click.secho(""  2. Ensure your CA bundle file is in .pem, .crt, or .cer format"", fg=""yellow"")
+        click.secho(""  3. Contact your system administrator for the correct CA bundle"", fg=""yellow"")
         return None
     except requests.RequestException as e:
         click.secho(f""Error fetching provider data: {e}"", fg=""red"")