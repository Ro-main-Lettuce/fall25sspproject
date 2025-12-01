@@ -176,6 +176,7 @@ def test_ad_sets_stream(self, http_mocker: HttpMocker):
             ""bid_constraints"",
             ""adlabels"",
             ""learning_stage_info"",
+            ""attribution_spec"",
         ]
 
         http_mocker.get(