@@ -37,7 +37,7 @@
 PROVIDER = ""yidun""
 
 
-RISK_LABLES = {
+RISK_LABELS = {
     100: ""色情"",
     200: ""广告"",
     260: ""广告法"",
@@ -109,7 +109,7 @@ def yidun_check(app: Flask, data_id: str, content: str, user_id: str = None):
                     .get(""suggestion"", YIDUN_RESULT_SUGGESTION_PASS)
                 ),
                 risk_labels=[
-                    RISK_LABLES.get(
+                    RISK_LABELS.get(
                         response_json.get(""result"", {})
                         .get(""antispam"", {})
                         .get(""label"", 100),