@@ -57,7 +57,8 @@ def create_job_creation_request(shop_name: str, lower_boundary: datetime, upper_
 def create_job_status_request(shop_name: str, job_id: str) -> HttpRequest:
     return HttpRequest(
         url=_create_job_url(shop_name),
-        body=f""""""query {{
+        body={
+            ""query"": f""""""query {{
                     node(id: ""{job_id}"") {{
                         ... on BulkOperation {{
                             id
@@ -70,14 +71,16 @@ def create_job_status_request(shop_name: str, job_id: str) -> HttpRequest:
                             partialDataUrl
                         }}
                     }}
-                }}"""""",
+                }}""""""
+        },
     )
 
 
 def create_job_cancel_request(shop_name: str, job_id: str) -> HttpRequest:
     return HttpRequest(
         url=_create_job_url(shop_name),
-        body=f""""""mutation {{
+        body={
+            ""query"": f""""""mutation {{
                 bulkOperationCancel(id: ""{job_id}"") {{
                     bulkOperation {{
                         id
@@ -89,7 +92,8 @@ def create_job_cancel_request(shop_name: str, job_id: str) -> HttpRequest:
                         message
                     }}
                 }}
-            }}"""""",
+            }}""""""
+        },
     )
 
 