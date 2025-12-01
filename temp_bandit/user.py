@@ -3,7 +3,7 @@
 from flaskr.service.common.models import raise_param_error
 from flaskr.service.profile.funcs import (
     get_user_profile_labels,
-    update_user_profile_with_lable,
+    update_user_profile_with_label,
 )
 from ..service.user import (
     create_new_user,
@@ -379,7 +379,7 @@ def update_profile():
         if not profiles:
             raise_param_error(""profiles"")
         with app.app_context():
-            ret = update_user_profile_with_lable(
+            ret = update_user_profile_with_label(
                 app, request.user.user_id, profiles, update_all=True
             )
             db.session.commit()