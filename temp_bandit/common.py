@@ -14,7 +14,7 @@
 from flaskr.service.user.models import User
 from flaskr.service.profile.funcs import (
     get_user_profile_labels,
-    update_user_profile_with_lable,
+    update_user_profile_with_label,
 )
 from sqlalchemy import text
 from flaskr.api.sms.aliyun import send_sms_code_ali
@@ -106,11 +106,11 @@ def validate_user(app: Flask, token: str) -> UserInfo:
                 app.logger.info(""user_id:"" + user_id)
 
             app.logger.info(""user_id:"" + user_id)
-            redis_token = redis.get(app.config[""REDIS_KEY_PRRFIX_USER""] + user_id)
+            redis_token = redis.get(app.config[""REDIS_KEY_PREFIX_USER""] + user_id)
             if redis_token is None:
                 raise_error(""USER.USER_TOKEN_EXPIRED"")
             set_token = str(
-                redis.get(app.config[""REDIS_KEY_PRRFIX_USER""] + user_id),
+                redis.get(app.config[""REDIS_KEY_PREFIX_USER""] + user_id),
                 encoding=""utf-8"",
             )
             if set_token == token:
@@ -222,7 +222,7 @@ def require_reset_pwd_code(app: Flask, login: str):
         if user:
             code = random.randint(0, 9999)
             redis.set(
-                app.config[""REDIS_KEY_PRRFIX_RESET_PWD""] + user.user_id,
+                app.config[""REDIS_KEY_PREFIX_RESET_PWD""] + user.user_id,
                 code,
                 ex=app.config[""RESET_PWD_CODE_EXPIRE_TIME""],
             )
@@ -239,7 +239,7 @@ def reset_pwd(app: Flask, login: str, code: int, newpwd: str):
         ).first()
         if user:
             redis_code = redis.get(
-                app.config[""REDIS_KEY_PRRFIX_RESET_PWD""] + user.user_id
+                app.config[""REDIS_KEY_PREFIX_RESET_PWD""] + user.user_id
             )
             if redis_code is None:
                 raise_error(""USER.RESET_PWD_CODE_EXPIRED"")
@@ -262,13 +262,13 @@ def reset_pwd(app: Flask, login: str, code: int, newpwd: str):
 def get_sms_code_info(app: Flask, user_id: str, resend: bool):
     User = get_model(app)
     with app.app_context():
-        phone = redis.get(app.config[""REDIS_KEY_PRRFIX_PHONE""] + user_id)
+        phone = redis.get(app.config[""REDIS_KEY_PREFIX_PHONE""] + user_id)
         if phone is None:
             user = User.query.filter(User.user_id == user_id).first()
             phone = user.mobile
         else:
             phone = str(phone, encoding=""utf-8"")
-        ttl = redis.ttl(app.config[""REDIS_KEY_PRRFIX_PHONE_CODE""] + phone)
+        ttl = redis.ttl(app.config[""REDIS_KEY_PREFIX_PHONE_CODE""] + phone)
         if ttl < 0:
             ttl = 0
         return {""expire_in"": ttl, ""phone"": phone}
@@ -280,12 +280,12 @@ def send_sms_code_without_check(app: Flask, user_info: User, phone: str):
     random_string = """".join(random.choices(characters, k=4))
     # 发送短信验证码
     redis.set(
-        app.config[""REDIS_KEY_PRRFIX_PHONE""] + user_info.user_id,
+        app.config[""REDIS_KEY_PREFIX_PHONE""] + user_info.user_id,
         phone,
         ex=app.config.get(""PHONE_EXPIRE_TIME"", 60 * 30),
     )
     redis.set(
-        app.config[""REDIS_KEY_PRRFIX_PHONE_CODE""] + phone,
+        app.config[""REDIS_KEY_PREFIX_PHONE_CODE""] + phone,
         random_string,
         ex=app.config[""PHONE_CODE_EXPIRE_TIME""],
     )
@@ -297,7 +297,7 @@ def send_sms_code_without_check(app: Flask, user_info: User, phone: str):
 def verify_sms_code_without_phone(app: Flask, user_id: str, checkcode) -> UserToken:
     User = get_model(app)
     with app.app_context():
-        phone = redis.get(app.config[""REDIS_KEY_PRRFIX_PHONE""] + user_id)
+        phone = redis.get(app.config[""REDIS_KEY_PREFIX_PHONE""] + user_id)
         if phone is None:
             app.logger.info(""cache user_id:"" + user_id + "" phone is None"")
             user = (
@@ -361,13 +361,13 @@ def migrate_user_study_record(app: Flask, from_user_id: str, to_user_id: str):
 
 
 # verify sms code
-def verify_sms_code(app: Flask, user_id, phone: str, chekcode: str) -> UserToken:
+def verify_sms_code(app: Flask, user_id, phone: str, checkcode: str) -> UserToken:
     User = get_model(app)
-    check_save = redis.get(app.config[""REDIS_KEY_PRRFIX_PHONE_CODE""] + phone)
-    if check_save is None and chekcode != FIX_CHECK_CODE:
+    check_save = redis.get(app.config[""REDIS_KEY_PREFIX_PHONE_CODE""] + phone)
+    if check_save is None and checkcode != FIX_CHECK_CODE:
         raise_error(""USER.SMS_SEND_EXPIRED"")
     check_save_str = str(check_save, encoding=""utf-8"") if check_save else """"
-    if chekcode != check_save_str and chekcode != FIX_CHECK_CODE:
+    if checkcode != check_save_str and checkcode != FIX_CHECK_CODE:
         raise_error(""USER.SMS_CHECK_ERROR"")
     else:
         user_info = (
@@ -384,7 +384,7 @@ def verify_sms_code(app: Flask, user_id, phone: str, chekcode: str) -> UserToken
             )
         elif user_id != user_info.user_id:
             new_profiles = get_user_profile_labels(app, user_id)
-            update_user_profile_with_lable(app, user_info.user_id, new_profiles)
+            update_user_profile_with_label(app, user_info.user_id, new_profiles)
             origin_user = User.query.filter(User.user_id == user_id).first()
             migrate_user_study_record(app, origin_user.user_id, user_info.user_id)
             if (