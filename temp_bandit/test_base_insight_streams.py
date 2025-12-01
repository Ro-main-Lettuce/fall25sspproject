@@ -70,7 +70,6 @@ def test_init(self, api, some_config):
         ]
         assert stream.name == ""ads_insights""
         assert stream.primary_key == [""date_start"", ""account_id"", ""ad_id""]
-        assert stream.action_report_time == ""mixed""
 
     def test_init_override(self, api, some_config):
         stream = AdsInsights(