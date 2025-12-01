@@ -8,6 +8,7 @@
 from responses.registries import OrderedRegistry
 from source_github.source import SourceGithub
 
+
 @pytest.mark.usefixtures(""mitmproxy_cache"")
 def test_http_caching():
     """"""Test that HTTP requests are cached when using mitmproxy.""""""