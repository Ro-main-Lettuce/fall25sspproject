@@ -1,28 +1,30 @@
 import os
-import requests
 from typing import Any
 
+import requests
+
 from .exa_base_tool import EXABaseTool
 
+
 class EXASearchTool(EXABaseTool):
-  def _run(
-    self,
-    **kwargs: Any,
-  ) -> Any:
-    search_query = kwargs.get('search_query')
-    if search_query is None:
-      search_query = kwargs.get('query')
+    def _run(
+        self,
+        **kwargs: Any,
+    ) -> Any:
+        search_query = kwargs.get(""search_query"")
+        if search_query is None:
+            search_query = kwargs.get(""query"")
 
-    payload = {
-        ""query"": search_query,
-        ""type"": ""magic"",
-    }
+        payload = {
+            ""query"": search_query,
+            ""type"": ""magic"",
+        }
 
-    headers = self.headers.copy()
-    headers[""x-api-key""] = os.environ['EXA_API_KEY']
+        headers = self.headers.copy()
+        headers[""x-api-key""] = os.environ[""EXA_API_KEY""]
 
-    response = requests.post(self.search_url, json=payload, headers=headers)
-    results = response.json()
-    if 'results' in results:
-      results = super()._parse_results(results['results'])
-    return results
+        response = requests.post(self.search_url, json=payload, headers=headers)
+        results = response.json()
+        if ""results"" in results:
+            results = super()._parse_results(results[""results""])
+        return results