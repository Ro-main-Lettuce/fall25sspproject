@@ -1,33 +1,59 @@
 from __future__ import annotations
 
 import urllib.parse
+from typing import TYPE_CHECKING, final
 
 import requests
 from requests.adapters import HTTPAdapter
+from requests.auth import AuthBase
+from typing_extensions import override
 
 from fixtures.log_helper import log
 
+if TYPE_CHECKING:
+    from requests import PreparedRequest
 
+
+@final
+class BearerAuth(AuthBase):
+    """"""
+    Auth implementation for bearer authorization in HTTP requests through the
+    requests HTTP client library.
+    """"""
+
+    def __init__(self, jwt: str):
+        self.__jwt = jwt
+
+    @override
+    def __call__(self, request: PreparedRequest) -> PreparedRequest:
+        request.headers[""Authorization""] = ""Bearer "" + self.__jwt
+        return request
+
+
+@final
 class EndpointHttpClient(requests.Session):
     def __init__(
         self,
         external_port: int,
         internal_port: int,
+        jwt: str,
     ):
         super().__init__()
         self.external_port: int = external_port
         self.internal_port: int = internal_port
+        self.auth = BearerAuth(jwt)
 
         self.mount(""http://"", HTTPAdapter())
 
     def dbs_and_roles(self):
-        res = self.get(f""http://localhost:{self.external_port}/dbs_and_roles"")
+        res = self.get(f""http://localhost:{self.external_port}/dbs_and_roles"", auth=self.auth)
         res.raise_for_status()
         return res.json()
 
     def database_schema(self, database: str):
         res = self.get(
-            f""http://localhost:{self.external_port}/database_schema?database={urllib.parse.quote(database, safe='')}""
+            f""http://localhost:{self.external_port}/database_schema?database={urllib.parse.quote(database, safe='')}"",
+            auth=self.auth,
         )
         res.raise_for_status()
         return res.text
@@ -58,13 +84,13 @@ def metrics(self) -> str:
 
     # Current compute status.
     def status(self):
-        res = self.get(f""http://localhost:{self.external_port}/status"")
+        res = self.get(f""http://localhost:{self.external_port}/status"", auth=self.auth)
         res.raise_for_status()
         return res.json()
 
     # Compute startup-related metrics.
     def metrics_json(self):
-        res = self.get(f""http://localhost:{self.external_port}/metrics.json"")
+        res = self.get(f""http://localhost:{self.external_port}/metrics.json"", auth=self.auth)
         res.raise_for_status()
         return res.json()
 