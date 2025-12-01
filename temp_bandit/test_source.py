@@ -6,9 +6,10 @@
 import logging
 from unittest.mock import patch
 
+import freezegun
 import pytest
 from source_amazon_seller_partner import SourceAmazonSellerPartner
-from source_amazon_seller_partner.streams import VendorOrders
+from source_amazon_seller_partner.components import AmazonSPOauthAuthenticator
 from source_amazon_seller_partner.utils import AmazonConfigException
 
 from airbyte_cdk.sources.streams import Stream
@@ -75,19 +76,6 @@ def connector_config_without_start_date():
     }
 
 
-def test_check_connection_with_vendor_report(mocker, requests_mock, connector_vendor_config_with_report_options):
-    mocker.patch(""time.sleep"", lambda x: None)
-    requests_mock.register_uri(
-        ""POST"",
-        ""https://api.amazon.com/auth/o2/token"",
-        status_code=200,
-        json={""access_token"": ""access_token"", ""expires_in"": ""3600""},
-    )
-
-    with patch.object(VendorOrders, ""read_records"", return_value=iter([{""some_key"": ""some_value""}])):
-        assert SourceAmazonSellerPartner().check_connection(logger, connector_vendor_config_with_report_options) == (True, None)
-
-
 def test_check_connection_with_orders_stop_iteration(requests_mock, connector_config_with_report_options):
     requests_mock.register_uri(
         ""POST"",
@@ -101,7 +89,11 @@ def test_check_connection_with_orders_stop_iteration(requests_mock, connector_co
         status_code=201,
         json={""payload"": {""Orders"": []}},
     )
-    assert SourceAmazonSellerPartner().check_connection(logger, connector_config_with_report_options) == (True, None)
+    assert SourceAmazonSellerPartner(
+        config=connector_config_with_report_options,
+        catalog=None,
+        state=None,
+    ).check_connection(logger, connector_config_with_report_options) == (True, None)
 
 
 def test_check_connection_with_orders(requests_mock, connector_config_with_report_options):
@@ -115,9 +107,13 @@ def test_check_connection_with_orders(requests_mock, connector_config_with_repor
         ""GET"",
         ""https://sandbox.sellingpartnerapi-na.amazon.com/orders/v0/orders"",
         status_code=200,
-        json={""payload"": {""Orders"": [{""LastUpdateDate"": ""2024-06-02""}]}},
+        json={""payload"": {""Orders"": [{""LastUpdateDate"": ""2024-06-02T00:00:00Z""}]}},
     )
-    assert SourceAmazonSellerPartner().check_connection(logger, connector_config_with_report_options) == (True, None)
+    assert SourceAmazonSellerPartner(
+        config=connector_config_with_report_options,
+        catalog=None,
+        state=None,
+    ).check_connection(logger, connector_config_with_report_options) == (True, None)
 
 
 @pytest.mark.parametrize(
@@ -140,15 +136,25 @@ def test_check_connection_with_orders(requests_mock, connector_config_with_repor
 )
 def test_get_stream_report_options_list(connector_config_with_report_options, report_name, stream_name_w_options):
     assert (
-        list(SourceAmazonSellerPartner().get_stream_report_kwargs(report_name, connector_config_with_report_options))
+        list(
+            SourceAmazonSellerPartner(
+                config=connector_config_with_report_options,
+                catalog=None,
+                state=None,
+            ).get_stream_report_kwargs(report_name, connector_config_with_report_options)
+        )
         == stream_name_w_options
     )
 
 
 def test_config_report_options_validation_error_duplicated_streams(connector_config_with_report_options):
     connector_config_with_report_options[""report_options_list""].append(connector_config_with_report_options[""report_options_list""][0])
     with pytest.raises(AmazonConfigException) as e:
-        SourceAmazonSellerPartner().validate_stream_report_options(connector_config_with_report_options)
+        SourceAmazonSellerPartner(
+            config=connector_config_with_report_options,
+            catalog=None,
+            state=None,
+        ).validate_stream_report_options(connector_config_with_report_options)
     assert e.value.message == ""Stream name should be unique among all Report options list""
 
 
@@ -157,20 +163,30 @@ def test_config_report_options_validation_error_duplicated_options(connector_con
         connector_config_with_report_options[""report_options_list""][0][""options_list""][0]
     )
     with pytest.raises(AmazonConfigException) as e:
-        SourceAmazonSellerPartner().validate_stream_report_options(connector_config_with_report_options)
+        SourceAmazonSellerPartner(
+            config=connector_config_with_report_options,
+            catalog=None,
+            state=None,
+        ).validate_stream_report_options(connector_config_with_report_options)
     assert e.value.message == ""Option names should be unique for `GET_FBA_FULFILLMENT_CUSTOMER_RETURNS_DATA` report options""
 
 
 def test_streams(connector_config_without_start_date):
-    for stream in SourceAmazonSellerPartner().streams(connector_config_without_start_date):
+    for stream in SourceAmazonSellerPartner(
+        config=connector_config_without_start_date,
+        catalog=None,
+        state=None,
+    ).streams(connector_config_without_start_date):
         assert isinstance(stream, Stream)
 
 
-@pytest.mark.parametrize((""deployment_mode"", ""expected_streams_count""), ((""cloud"", 44), (""oss"", 53)))
-def test_streams_count(deployment_mode, expected_streams_count, connector_config_without_start_date, monkeypatch):
-    monkeypatch.setenv(""DEPLOYMENT_MODE"", deployment_mode)
-    streams = SourceAmazonSellerPartner().streams(connector_config_without_start_date)
-    assert len(streams) == expected_streams_count
+def test_streams_count(connector_config_without_start_date, monkeypatch):
+    streams = SourceAmazonSellerPartner(
+        config=connector_config_without_start_date,
+        catalog=None,
+        state=None,
+    ).streams(connector_config_without_start_date)
+    assert len(streams) == 44
 
 
 @pytest.mark.parametrize(
@@ -186,28 +202,34 @@ def test_streams_count(deployment_mode, expected_streams_count, connector_config
 def test_replication_dates_validation(config, should_raise):
     if should_raise:
         with pytest.raises(AmazonConfigException) as e:
-            SourceAmazonSellerPartner().validate_replication_dates(config)
+            SourceAmazonSellerPartner(
+                config=config,
+                catalog=None,
+                state=None,
+            ).validate_replication_dates(config)
         assert e.value.message == ""End Date should be greater than or equal to Start Date""
     else:
-        assert SourceAmazonSellerPartner().validate_replication_dates(config) is None
-
-
-@pytest.mark.parametrize((""deployment_mode"", ""common_streams_count""), ((""cloud"", 0), (""oss"", 8)))
-def test_spec(deployment_mode, common_streams_count, monkeypatch):
-    monkeypatch.setenv(""DEPLOYMENT_MODE"", deployment_mode)
-    oss_only_streams = {
-        ""GET_BRAND_ANALYTICS_MARKET_BASKET_REPORT"",
-        ""GET_BRAND_ANALYTICS_SEARCH_TERMS_REPORT"",
-        ""GET_BRAND_ANALYTICS_REPEAT_PURCHASE_REPORT"",
-        ""GET_SALES_AND_TRAFFIC_REPORT"",
-        ""GET_VENDOR_SALES_REPORT"",
-        ""GET_VENDOR_INVENTORY_REPORT"",
-        ""GET_VENDOR_NET_PURE_PRODUCT_MARGIN_REPORT"",
-        ""GET_VENDOR_TRAFFIC_REPORT"",
-    }
-    streams_with_report_options = (
-        SourceAmazonSellerPartner()
-        .spec(logger)
-        .connectionSpecification[""properties""][""report_options_list""][""items""][""properties""][""report_name""][""enum""]
-    )
-    assert len(set(streams_with_report_options).intersection(oss_only_streams)) == common_streams_count
+        assert (
+            SourceAmazonSellerPartner(
+                config=config,
+                catalog=None,
+                state=None,
+            ).validate_replication_dates(config)
+            is None
+        )
+
+
+@freezegun.freeze_time(""2024-01-01T00:00:00"")
+def test_get_stream_kwargs(connector_config_with_report_options):
+    kwargs = SourceAmazonSellerPartner(
+        config=connector_config_with_report_options,
+        catalog=None,
+        state=None,
+    )._get_stream_kwargs(config=connector_config_with_report_options)
+
+    assert kwargs[""url_base""] == ""https://sandbox.sellingpartnerapi-na.amazon.com""
+    assert isinstance(kwargs[""authenticator""], AmazonSPOauthAuthenticator)
+    assert kwargs[""replication_start_date""] == ""2022-01-01T00:00:00Z""
+    assert kwargs[""marketplace_id""] == ""ATVPDKIKX0DER""
+    assert kwargs[""period_in_days""] == 365
+    assert kwargs[""replication_end_date""] is None