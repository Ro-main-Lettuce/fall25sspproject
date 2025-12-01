@@ -18,7 +18,7 @@
 TIME_ZONE = pytz.timezone(""Asia/Shanghai"")
 
 
-def get_tenat_token(app: Flask, app_id=APPID, app_secrect=APP_SECRET):
+def get_tenant_token(app: Flask, app_id=APPID, app_secret=APP_SECRET):
     from ...dao import redis_client as redis
 
     token = redis.get(REDIS_KEY_PREFIX + app_id + ""token"")
@@ -27,7 +27,7 @@ def get_tenat_token(app: Flask, app_id=APPID, app_secrect=APP_SECRET):
         return str(token, encoding=""utf-8"")
     url = ""https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/""
     headers = {""Content-Type"": ""application/json""}
-    data = {""app_id"": app_id, ""app_secret"": app_secrect}
+    data = {""app_id"": app_id, ""app_secret"": app_secret}
     r = requests.post(url, headers=headers, data=json.dumps(data))
     app.logger.info(""get_tenat_token:"" + str(r.status_code))
     app.logger.info(""get_tenat_token:"" + str(r.text))
@@ -39,7 +39,7 @@ def get_tenat_token(app: Flask, app_id=APPID, app_secrect=APP_SECRET):
 
 def create_document(app: Flask, title: str):
 
-    token = get_tenat_token(app)
+    token = get_tenant_token(app)
     url = ""https://open.feishu.cn/open-apis/docx/v1/documents""
     headers = {""Content-Type"": ""application/json"", ""Authorization"": ""Bearer "" + token}
     data = {
@@ -54,7 +54,7 @@ def create_document(app: Flask, title: str):
 
 
 def update_document_to_public(app: Flask, doc_id: str):
-    token = get_tenat_token(app)
+    token = get_tenant_token(app)
     url = ""https://open.feishu.cn/open-apis/drive/v2/permissions/{doc_id}/public?type=docx"".format(
         doc_id=doc_id
     )
@@ -71,7 +71,7 @@ def update_document_to_public(app: Flask, doc_id: str):
 
 
 def add_text_element(app: Flask, doc_id: str, user_name: str, text: str):
-    token = get_tenat_token(app)
+    token = get_tenant_token(app)
     url = ""https://open.feishu.cn/open-apis/docx/v1/documents/{doc_id}/blocks/{doc_id}/children"".format(
         doc_id=doc_id
     )
@@ -108,7 +108,7 @@ def add_text_element(app: Flask, doc_id: str, user_name: str, text: str):
 
 
 def remove_text_element(app: Flask, doc_id: str, block_id: str):
-    token = get_tenat_token(app)
+    token = get_tenant_token(app)
 
     url = ""https://open.feishu.cn/open-apis/docx/v1/documents/{document_id}/blocks/{block_id}"".format(
         document_id=doc_id, block_id=doc_id
@@ -147,7 +147,7 @@ def remove_text_element(app: Flask, doc_id: str, block_id: str):
 
 
 def get_document_info(app: Flask, doc_id: str, block_id: str):
-    token = get_tenat_token(app)
+    token = get_tenant_token(app)
     url = ""https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables"".format(
         app_token=doc_id
     )
@@ -159,7 +159,7 @@ def get_document_info(app: Flask, doc_id: str, block_id: str):
 
 
 def list_views(app: Flask, app_token: str, table_id: str):
-    token = get_tenat_token(app)
+    token = get_tenant_token(app)
     # https://open.feishu.cn/open-apis/bitable/v1/apps/:app_token/tables/:table_id/views
     url = ""https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/views"".format(
         app_token=app_token, table_id=table_id
@@ -179,9 +179,9 @@ def list_records(
     page_token: str = None,
     page_size: int = None,
     app_id=APPID,
-    app_secrect=APP_SECRET,
+    app_secret=APP_SECRET,
 ):
-    token = get_tenat_token(app, app_id=app_id, app_secrect=app_secrect)
+    token = get_tenant_token(app, app_id=app_id, app_secret=app_secret)
     # https://open.feishu.cn/open-apis/bitable/v1/apps/:app_token/tables/:table_id/records/search
     url = ""https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/search"".format(
         app_token=app_token, table_id=table_id
@@ -212,7 +212,7 @@ def list_records(
 
 
 def list_tables(app: Flask, app_token: str):
-    token = get_tenat_token(app)
+    token = get_tenant_token(app)
     url = ""https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables"".format(
         app_token=app_token
     )