@@ -2,31 +2,13 @@
 
 
 from datetime import date
-from enum import Enum
 from typing import List, Optional
 
 from pydantic.v1 import Field
 
 from airbyte_cdk.sources.config import BaseConfig
 
 
-class StateFilterEnum(str, Enum):
-    enabled = ""enabled""
-    paused = ""paused""
-    archived = ""archived""
-
-
-class ReportRecordTypeEnum(str, Enum):
-    adGroups = ""adGroups""
-    asins = ""asins""
-    asins_keywords = ""asins_keywords""
-    asins_targets = ""asins_targets""
-    campaigns = ""campaigns""
-    keywords = ""keywords""
-    productAds = ""productAds""
-    targets = ""targets""
-
-
 class SourceAmazonAdsSpec(BaseConfig):
     class Config:
         title = ""Source Amazon Ads""
@@ -81,24 +63,10 @@ class Config:
         title=""Marketplace IDs"",
         order=7,
     )
-    state_filter: Optional[List[StateFilterEnum]] = Field(
-        default=[],
-        description=""Reflects the state of the Display, Product, and Brand Campaign streams as enabled, paused, or archived. If you do not populate this field, it will be ignored completely."",
-        title=""State Filter"",
-        unique_items=True,
-        order=8,
-    )
     look_back_window: Optional[int] = Field(
         3,
         description=""The amount of days to go back in time to get the updated data from Amazon Ads"",
         examples=[3, 10],
         title=""Look Back Window"",
-        order=9,
-    )
-    report_record_types: Optional[List[ReportRecordTypeEnum]] = Field(
-        [],
-        description='Optional configuration which accepts an array of string of record types. Leave blank for default behaviour to pull all report types. Use this config option only if you want to pull specific report type(s). See <a href=""https://advertising.amazon.com/API/docs/en-us/reporting/v2/report-types"">docs</a> for more details',
-        title=""Report Record Types"",
-        unique_items=True,
-        order=10,
+        order=8,
     )