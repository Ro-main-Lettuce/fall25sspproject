@@ -1,18 +1,27 @@
-#
-# Copyright (c) 2023 Airbyte, Inc., all rights reserved.
-#
-
-from http import HTTPStatus
-from typing import Any, List, Mapping
-
-import requests
-
-from airbyte_cdk.sources.streams.http.requests_native_auth import Oauth2Authenticator
-from source_amazon_ads.streams.report_streams.report_stream_models import ReportInfo
-from source_amazon_ads.streams.report_streams.report_streams import ReportStream
+# Copyright (c) 2024 Airbyte, Inc., all rights reserved.
 
+BRANDS_METRICS_MAP_V3 = {
+    ""purchasedAsin"": [
+        ""campaignBudgetCurrencyCode"",
+        ""campaignName"",
+        ""adGroupName"",
+        ""attributionType"",
+        ""purchasedAsin"",
+        ""productName"",
+        ""productCategory"",
+        ""sales14d"",
+        ""orders14d"",
+        ""unitsSold14d"",
+        ""newToBrandSales14d"",
+        ""newToBrandPurchases14d"",
+        ""newToBrandUnitsSold14d"",
+        ""newToBrandSalesPercentage14d"",
+        ""newToBrandPurchasesPercentage14d"",
+        ""newToBrandUnitsSoldPercentage14d"",
+    ]
+}
 
-METRICS_MAP_V3 = {
+DISPLAY_REPORT_METRICS_MAP = {
     ""campaigns"": [
         ""addToCart"",
         ""addToCartClicks"",
@@ -308,76 +317,234 @@
     ],
 }
 
-
-METRICS_TYPE_TO_ID_MAP = {""campaigns"": ""campaignId"", ""adGroups"": ""adGroupId"", ""productAds"": ""adId"", ""targets"": ""targetId"", ""asins"": ""asin""}
-
-
-class SponsoredDisplayReportStream(ReportStream):
-    """"""
-    https://advertising.amazon.com/API/docs/en-us/sponsored-display/3-0/openapi#/Reports
-    """"""
-
-    API_VERSION = ""reporting""  # v3
-    REPORT_DATE_FORMAT = ""YYYY-MM-DD""
-    ad_product = ""SPONSORED_DISPLAY""
-    report_is_created = HTTPStatus.OK
-    metrics_map = METRICS_MAP_V3
-    metrics_type_to_id_map = METRICS_TYPE_TO_ID_MAP
-
-    def __init__(self, config: Mapping[str, Any], profiles: List[dict[str, Any]], authenticator: Oauth2Authenticator):
-        super().__init__(config, profiles, authenticator)
-        # using session without auth as API returns 400 bad request if Authorization header presents in request
-        # X-Amz-Algorithm and X-Amz-Signature query params already present in the url, that is enough to make proper request
-        self._report_download_session = requests.Session()
-
-    def report_init_endpoint(self, record_type: str) -> str:
-        return f""/{self.API_VERSION}/reports""
-
-    def _download_report(self, report_info: ReportInfo, url: str) -> List[dict]:
-        """"""
-        Download and parse report result
-        """"""
-        return super()._download_report(None, url)
-
-    def _get_init_report_body(self, report_date: str, record_type: str, profile):
-        metrics_list = self.metrics_map[record_type]
-
-        reportTypeId = ""sdCampaigns""  # SponsoredDisplayCampaigns
-        group_by = [""campaign""]
-        filters = []
-
-        if record_type == ""adGroups"":
-            reportTypeId = ""sdAdGroup""
-            group_by = [""adGroup""]
-
-        elif record_type == ""productAds"":
-            reportTypeId = ""sdAdvertisedProduct""
-            group_by = [""advertiser""]
-
-        elif record_type == ""asins"":
-            reportTypeId = ""sdPurchasedProduct""
-            group_by = [""asin""]
-
-        elif record_type == ""keywords"" or record_type == ""targets"":
-            group_by = [""targeting""]
-            reportTypeId = ""sdTargeting""
-
-            if record_type == ""keywords"":
-                filters = [{""field"": ""keywordType"", ""values"": [""BROAD"", ""PHRASE"", ""EXACT""]}]
-
-        body = {
-            ""name"": f""{record_type} report {report_date}"",
-            ""startDate"": report_date,
-            ""endDate"": report_date,
-            ""configuration"": {
-                ""adProduct"": self.ad_product,
-                ""groupBy"": group_by,
-                ""columns"": metrics_list,
-                ""reportTypeId"": reportTypeId,
-                ""filters"": filters,
-                ""timeUnit"": ""SUMMARY"",
-                ""format"": ""GZIP_JSON"",
-            },
-        }
-
-        yield body
+PRODUCTS_REPORT_METRICS_MAP = {
+    ""campaigns"": [
+        ""campaignName"",
+        ""campaignId"",
+        ""campaignStatus"",
+        ""campaignBudgetAmount"",
+        ""campaignRuleBasedBudgetAmount"",
+        ""campaignApplicableBudgetRuleId"",
+        ""campaignApplicableBudgetRuleName"",
+        ""impressions"",
+        ""clicks"",
+        ""cost"",
+        ""purchases1d"",
+        ""purchases7d"",
+        ""purchases14d"",
+        ""purchases30d"",
+        ""purchasesSameSku1d"",
+        ""purchasesSameSku7d"",
+        ""purchasesSameSku14d"",
+        ""purchasesSameSku30d"",
+        ""unitsSoldClicks1d"",
+        ""unitsSoldClicks7d"",
+        ""unitsSoldClicks14d"",
+        ""unitsSoldClicks30d"",
+        ""sales1d"",
+        ""sales7d"",
+        ""sales14d"",
+        ""sales30d"",
+        ""attributedSalesSameSku1d"",
+        ""attributedSalesSameSku7d"",
+        ""attributedSalesSameSku14d"",
+        ""attributedSalesSameSku30d"",
+        ""unitsSoldSameSku1d"",
+        ""unitsSoldSameSku7d"",
+        ""unitsSoldSameSku14d"",
+        ""unitsSoldSameSku30d"",
+    ],
+    ""adGroups"": [
+        ""campaignName"",
+        ""campaignId"",
+        ""adGroupName"",
+        ""adGroupId"",
+        ""impressions"",
+        ""clicks"",
+        ""cost"",
+        ""purchases1d"",
+        ""purchases7d"",
+        ""purchases14d"",
+        ""purchases30d"",
+        ""purchasesSameSku1d"",
+        ""purchasesSameSku7d"",
+        ""purchasesSameSku14d"",
+        ""purchasesSameSku30d"",
+        ""unitsSoldClicks1d"",
+        ""unitsSoldClicks7d"",
+        ""unitsSoldClicks14d"",
+        ""unitsSoldClicks30d"",
+        ""sales1d"",
+        ""sales7d"",
+        ""sales14d"",
+        ""sales30d"",
+        ""attributedSalesSameSku1d"",
+        ""attributedSalesSameSku7d"",
+        ""attributedSalesSameSku14d"",
+        ""attributedSalesSameSku30d"",
+        ""unitsSoldSameSku1d"",
+        ""unitsSoldSameSku7d"",
+        ""unitsSoldSameSku14d"",
+        ""unitsSoldSameSku30d"",
+    ],
+    ""keywords"": [
+        ""campaignName"",
+        ""campaignId"",
+        ""adGroupName"",
+        ""adGroupId"",
+        ""keywordId"",
+        ""keyword"",
+        ""matchType"",
+        ""impressions"",
+        ""clicks"",
+        ""cost"",
+        ""purchases1d"",
+        ""purchases7d"",
+        ""purchases14d"",
+        ""purchases30d"",
+        ""purchasesSameSku1d"",
+        ""purchasesSameSku7d"",
+        ""purchasesSameSku14d"",
+        ""purchasesSameSku30d"",
+        ""unitsSoldClicks1d"",
+        ""unitsSoldClicks7d"",
+        ""unitsSoldClicks14d"",
+        ""unitsSoldClicks30d"",
+        ""sales1d"",
+        ""sales7d"",
+        ""sales14d"",
+        ""sales30d"",
+        ""attributedSalesSameSku1d"",
+        ""attributedSalesSameSku7d"",
+        ""attributedSalesSameSku14d"",
+        ""attributedSalesSameSku30d"",
+        ""unitsSoldSameSku1d"",
+        ""unitsSoldSameSku7d"",
+        ""unitsSoldSameSku14d"",
+        ""unitsSoldSameSku30d"",
+    ],
+    ""targets"": [
+        ""campaignName"",
+        ""campaignId"",
+        ""adGroupName"",
+        ""adGroupId"",
+        ""keywordId"",
+        ""keyword"",
+        ""targeting"",
+        ""keywordType"",
+        ""impressions"",
+        ""clicks"",
+        ""cost"",
+        ""purchases1d"",
+        ""purchases7d"",
+        ""purchases14d"",
+        ""purchases30d"",
+        ""purchasesSameSku1d"",
+        ""purchasesSameSku7d"",
+        ""purchasesSameSku14d"",
+        ""purchasesSameSku30d"",
+        ""unitsSoldClicks1d"",
+        ""unitsSoldClicks7d"",
+        ""unitsSoldClicks14d"",
+        ""unitsSoldClicks30d"",
+        ""sales1d"",
+        ""sales7d"",
+        ""sales14d"",
+        ""sales30d"",
+        ""attributedSalesSameSku1d"",
+        ""attributedSalesSameSku7d"",
+        ""attributedSalesSameSku14d"",
+        ""attributedSalesSameSku30d"",
+        ""unitsSoldSameSku1d"",
+        ""unitsSoldSameSku7d"",
+        ""unitsSoldSameSku14d"",
+        ""unitsSoldSameSku30d"",
+    ],
+    ""productAds"": [
+        ""campaignName"",
+        ""campaignId"",
+        ""adGroupName"",
+        ""adGroupId"",
+        ""adId"",
+        ""impressions"",
+        ""clicks"",
+        ""cost"",
+        ""campaignBudgetCurrencyCode"",
+        ""advertisedAsin"",
+        ""purchases1d"",
+        ""purchases7d"",
+        ""purchases14d"",
+        ""purchases30d"",
+        ""purchasesSameSku1d"",
+        ""purchasesSameSku7d"",
+        ""purchasesSameSku14d"",
+        ""purchasesSameSku30d"",
+        ""unitsSoldClicks1d"",
+        ""unitsSoldClicks7d"",
+        ""unitsSoldClicks14d"",
+        ""unitsSoldClicks30d"",
+        ""sales1d"",
+        ""sales7d"",
+        ""sales14d"",
+        ""sales30d"",
+        ""attributedSalesSameSku1d"",
+        ""attributedSalesSameSku7d"",
+        ""attributedSalesSameSku14d"",
+        ""attributedSalesSameSku30d"",
+        ""unitsSoldSameSku1d"",
+        ""unitsSoldSameSku7d"",
+        ""unitsSoldSameSku14d"",
+        ""unitsSoldSameSku30d"",
+    ],
+    ""asins_keywords"": [
+        ""campaignName"",
+        ""campaignId"",
+        ""adGroupName"",
+        ""adGroupId"",
+        ""keywordId"",
+        ""keyword"",
+        ""advertisedAsin"",
+        ""purchasedAsin"",
+        ""advertisedSku"",
+        ""campaignBudgetCurrencyCode"",
+        ""matchType"",
+        ""unitsSoldClicks1d"",
+        ""unitsSoldClicks7d"",
+        ""unitsSoldClicks14d"",
+        ""unitsSoldClicks30d"",
+        ""unitsSoldOtherSku1d"",
+        ""unitsSoldOtherSku7d"",
+        ""unitsSoldOtherSku14d"",
+        ""unitsSoldOtherSku30d"",
+        ""salesOtherSku1d"",
+        ""salesOtherSku7d"",
+        ""salesOtherSku14d"",
+        ""salesOtherSku30d"",
+    ],
+    ""asins_targets"": [
+        ""campaignName"",
+        ""campaignId"",
+        ""adGroupName"",
+        ""adGroupId"",
+        ""advertisedAsin"",
+        ""purchasedAsin"",
+        ""advertisedSku"",
+        ""campaignBudgetCurrencyCode"",
+        ""matchType"",
+        ""unitsSoldClicks1d"",
+        ""unitsSoldClicks7d"",
+        ""unitsSoldClicks14d"",
+        ""unitsSoldClicks30d"",
+        ""unitsSoldOtherSku1d"",
+        ""unitsSoldOtherSku7d"",
+        ""unitsSoldOtherSku14d"",
+        ""unitsSoldOtherSku30d"",
+        ""salesOtherSku1d"",
+        ""salesOtherSku7d"",
+        ""salesOtherSku14d"",
+        ""salesOtherSku30d"",
+        ""keywordId"",
+        ""targeting"",
+        ""keywordType"",
+    ],
+}