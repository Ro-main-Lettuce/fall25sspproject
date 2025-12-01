@@ -4,6 +4,7 @@
 
 from dataclasses import dataclass, field
 from datetime import datetime
+from enum import Enum
 from time import sleep, time
 from typing import Any, Final, Iterable, List, Mapping, Optional
 
@@ -23,6 +24,16 @@
 from .tools import END_OF_FILE, BulkTools
 
 
+class BulkOperationUserErrorCode(Enum):
+    """"""
+    Possible error codes that can be returned by BulkOperationUserError.
+    https://shopify.dev/docs/api/admin-graphql/latest/enums/BulkOperationUserErrorCode
+    """"""
+
+    INVALID = ""INVALID""
+    OPERATION_IN_PROGRESS = ""OPERATION_IN_PROGRESS""
+
+
 @dataclass
 class ShopifyBulkManager:
     http_client: HttpClient
@@ -246,8 +257,7 @@ def _job_cancel(self) -> None:
         _, canceled_response = self.http_client.send_request(
             http_method=""POST"",
             url=self.base_url,
-            data=ShopifyBulkTemplates.cancel(self._job_id),
-            headers={""Content-Type"": ""application/graphql""},
+            json={""query"": ShopifyBulkTemplates.cancel(self._job_id)},
             request_kwargs={},
         )
         # mark the job was self-canceled
@@ -405,8 +415,7 @@ def _job_track_running(self) -> None:
         _, response = self.http_client.send_request(
             http_method=""POST"",
             url=self.base_url,
-            data=ShopifyBulkTemplates.status(self._job_id),
-            headers={""Content-Type"": ""application/graphql""},
+            json={""query"": ShopifyBulkTemplates.status(self._job_id)},
             request_kwargs={},
         )
         self._job_healthcheck(response)
@@ -419,18 +428,17 @@ def _has_running_concurrent_job(self, errors: Optional[Iterable[Mapping[str, Any
         Error example:
         [
             {
+                'code': 'OPERATION_IN_PROGRESS',
                 'field': None,
                 'message': 'A bulk query operation for this app and shop is already in progress: gid://shopify/BulkOperation/4039184154813.',
             }
         ]
         """"""
-
-        concurrent_job_pattern = ""A bulk query operation for this app and shop is already in progress""
         # the errors are handled in `job_job_check_for_errors`
         if errors:
             for error in errors:
-                message = error.get(""message"", """") if isinstance(error, dict) else """"
-                if concurrent_job_pattern in message:
+                error_code = error.get(""code"", """") if isinstance(error, dict) else """"
+                if error_code == BulkOperationUserErrorCode.OPERATION_IN_PROGRESS.value:
                     return True
         return False
 