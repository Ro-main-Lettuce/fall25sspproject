@@ -4,29 +4,16 @@
 
 
 import pytest
-from source_amazon_seller_partner.streams import (
-    FlatFileSettlementV2Reports,
-    LedgerDetailedViewReports,
-    MerchantListingsFypReport,
-    MerchantListingsReports,
-    SellerFeedbackReports,
+from integration.utils import config, get_stream_by_name
+from source_amazon_seller_partner.components import (
+    FlatFileSettlementV2ReportsTypeTransformer,
+    LedgerDetailedViewReportsTypeTransformer,
+    MerchantListingsFypReportTypeTransformer,
+    MerchantReportsTypeTransformer,
+    SellerFeedbackReportsTypeTransformer,
 )
 
 
-def reports_stream(marketplace_id):
-    stream = SellerFeedbackReports(
-        stream_name=""SELLER_FEEDBACK_REPORTS"",
-        url_base=""https://test.url"",
-        replication_start_date=""2010-01-25T00:00:00Z"",
-        replication_end_date=""2017-02-25T00:00:00Z"",
-        marketplace_id=marketplace_id,
-        authenticator=None,
-        period_in_days=0,
-        report_options=None,
-    )
-    return stream
-
-
 INPUT_DATES = {
     ""YYYY-MM-DD"": [""2017-01-13"", ""2017-12-12"", ""2017-12-17"", ""2011-12-13""],
     ""D.M.YY"": [""13.1.17"", ""12.12.17"", ""17.12.17"", ""13.12.11""],
@@ -39,7 +26,7 @@ def reports_stream(marketplace_id):
 
 def parametrize_seller_feedback():
     result = []
-    for marketplace_id, date_format in SellerFeedbackReports.MARKETPLACE_DATE_FORMAT_MAP.items():
+    for marketplace_id, date_format in SellerFeedbackReportsTypeTransformer.MARKETPLACE_DATE_FORMAT_MAP.items():
         for index, input_date in enumerate(INPUT_DATES.get(date_format)):
             expected_date = EXPECTED_DATES[index]
             result.append(
@@ -55,9 +42,8 @@ def parametrize_seller_feedback():
 
 @pytest.mark.parametrize(""marketplace_id,input_data,expected_data"", parametrize_seller_feedback())
 def test_transform_seller_feedback(marketplace_id, input_data, expected_data):
-    stream = reports_stream(marketplace_id)
-    transformer = stream.transformer
-    schema = stream.get_json_schema()
+    transformer = SellerFeedbackReportsTypeTransformer(config={""marketplace_id"": marketplace_id})
+    schema = get_stream_by_name(""GET_SELLER_FEEDBACK_DATA"", config().build()).get_json_schema()
     transformer.transform(input_data, schema)
 
     assert input_data == expected_data
@@ -76,10 +62,9 @@ def test_transform_seller_feedback(marketplace_id, input_data, expected_data):
         ),
     ),
 )
-def test_transform_merchant_reports(report_init_kwargs, input_data, expected_data):
-    stream = MerchantListingsReports(**report_init_kwargs)
-    transformer = stream.transformer
-    schema = stream.get_json_schema()
+def test_transform_merchant_reports(input_data, expected_data):
+    transformer = MerchantReportsTypeTransformer()
+    schema = get_stream_by_name(""GET_MERCHANT_LISTINGS_ALL_DATA"", config().build()).get_json_schema()
     transformer.transform(input_data, schema)
     assert input_data == expected_data
 
@@ -97,10 +82,9 @@ def test_transform_merchant_reports(report_init_kwargs, input_data, expected_dat
         ),
     ),
 )
-def test_transform_merchant_fyp_reports(report_init_kwargs, input_data, expected_data):
-    stream = MerchantListingsFypReport(**report_init_kwargs)
-    transformer = stream.transformer
-    schema = stream.get_json_schema()
+def test_transform_merchant_fyp_reports(input_data, expected_data):
+    transformer = MerchantListingsFypReportTypeTransformer()
+    schema = get_stream_by_name(""GET_MERCHANTS_LISTINGS_FYP_REPORT"", config().build()).get_json_schema()
     transformer.transform(input_data, schema)
     assert input_data == expected_data
 
@@ -115,10 +99,9 @@ def test_transform_merchant_fyp_reports(report_init_kwargs, input_data, expected
         ({""Date"": """", ""dataEndTime"": ""2022-07-31""}, {""Date"": """", ""dataEndTime"": ""2022-07-31""}),
     ),
 )
-def test_transform_ledger_reports(report_init_kwargs, input_data, expected_data):
-    stream = LedgerDetailedViewReports(**report_init_kwargs)
-    transformer = stream.transformer
-    schema = stream.get_json_schema()
+def test_transform_ledger_reports(input_data, expected_data):
+    transformer = LedgerDetailedViewReportsTypeTransformer()
+    schema = get_stream_by_name(""GET_LEDGER_DETAIL_VIEW_DATA"", config().build()).get_json_schema()
     transformer.transform(input_data, schema)
     assert input_data == expected_data
 
@@ -134,8 +117,7 @@ def test_transform_ledger_reports(report_init_kwargs, input_data, expected_data)
     ),
 )
 def test_transform_settlement_reports(report_init_kwargs, input_data, expected_data):
-    stream = FlatFileSettlementV2Reports(**report_init_kwargs)
-    transformer = stream.transformer
-    schema = stream.get_json_schema()
+    transformer = FlatFileSettlementV2ReportsTypeTransformer()
+    schema = get_stream_by_name(""GET_V2_SETTLEMENT_REPORT_DATA_FLAT_FILE"", config().build()).get_json_schema()
     transformer.transform(input_data, schema)
     assert input_data == expected_data