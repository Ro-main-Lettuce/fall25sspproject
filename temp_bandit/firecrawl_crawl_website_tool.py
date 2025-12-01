@@ -107,7 +107,7 @@ def _run(
         crawling_options[""scrapeOptions""][""formats""] = formats
         crawling_options[""scrapeOptions""][""timeout""] = timeout
 
-        return self._firecrawl.crawl_url(url, crawling_options)
+        return self._firecrawl.crawl_url(url, **crawling_options)
 
 
 try: