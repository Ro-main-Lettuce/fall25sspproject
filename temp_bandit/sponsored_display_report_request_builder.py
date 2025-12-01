@@ -1,10 +1,10 @@
-# Copyright (c) 2023 Airbyte, Inc., all rights reserved.
+# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
 
 import json
 from collections import OrderedDict
 from typing import Any, Dict, List, Optional
 
-import pendulum
+from airbyte_cdk.utils.datetime_helpers import AirbyteDateTime
 
 from .base_request_builder import AmazonAdsBaseRequestBuilder
 
@@ -134,8 +134,8 @@ def request_body(self) -> Optional[str]:
 
         return json.dumps(body)
 
-    def with_report_date(self, report_date: pendulum.date) -> ""SponsoredDisplayReportRequestBuilder"":
-        self._report_date = report_date.format(""YYYY-MM-DD"")
+    def with_report_date(self, report_date: AirbyteDateTime) -> ""SponsoredDisplayReportRequestBuilder"":
+        self._report_date = report_date.strftime(""%Y-%m-%d"")
         return self
 
     def with_metrics(self, metrics: List[str]) -> ""SponsoredDisplayReportRequestBuilder"":