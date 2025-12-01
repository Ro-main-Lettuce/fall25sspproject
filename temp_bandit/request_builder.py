@@ -32,16 +32,6 @@ def create_report_endpoint(cls, report_name: str) -> RequestBuilder:
         }
         return cls(""reports/2021-06-30/reports"").with_body(json.dumps(request_body))
 
-    @classmethod
-    def create_vendor_traffic_report_endpoint(cls, report_name: str) -> RequestBuilder:
-        request_body = {
-            ""reportType"": report_name,
-            ""marketplaceIds"": [MARKETPLACE_ID],
-            ""dataStartTime"": ""2023-01-01T00:00:00Z"",
-            ""dataEndTime"": ""2023-01-01T23:59:59Z"",
-        }
-        return cls(""reports/2021-06-30/reports"").with_body(json.dumps(request_body))
-
     @classmethod
     def check_report_status_endpoint(cls, report_id: str) -> RequestBuilder:
         return cls(f""reports/2021-06-30/reports/{report_id}"")