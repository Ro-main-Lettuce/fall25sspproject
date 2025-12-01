@@ -59,11 +59,10 @@ def add(
     def _run(
         self,
         query: str,
-        **kwargs: Any,
     ) -> Any:
-        self._before_run(query, **kwargs)
+        self._before_run(query)
 
         return f""Relevant Content:
{self.adapter.query(query)}""
 
-    def _before_run(self, query, **kwargs):
+    def _before_run(self, query: str):
         pass