@@ -8,7 +8,12 @@
 from flaskr.service.profile.profile_manage import save_profile_item_defination
 from flaskr.service.profile.models import ProfileItem
 from flaskr.service.common.models import raise_error
-from flaskr.service.shifu.utils import get_existing_blocks, get_original_outline_tree
+from flaskr.service.shifu.utils import (
+    get_existing_blocks,
+    get_original_outline_tree,
+    change_block_status_to_history,
+    mark_block_to_delete,
+)
 from flaskr.util import generate_id
 from flaskr.dao import db
 from datetime import datetime
@@ -19,7 +24,6 @@
     STATUS_DELETE,
 )
 from flaskr.service.check_risk.funcs import check_text_with_risk_control
-from .utils import change_block_status_to_history
 import queue
 from flaskr.dao import redis_client
 
@@ -85,20 +89,18 @@ def get_block_list(app, user_id: str, outline_id: str):
 
 def delete_block(app, user_id: str, outline_id: str, block_id: str):
     with app.app_context():
-        block = AILessonScript.query.filter(
-            AILessonScript.lesson_id == outline_id,
-            AILessonScript.status.in_([STATUS_DRAFT]),
-            AILessonScript.script_id == block_id,
-        ).first()
-        if not block:
-            block = AILessonScript.query.filter(
+        block = (
+            AILessonScript.query.filter(
                 AILessonScript.lesson_id == outline_id,
-                AILessonScript.status.in_([STATUS_PUBLISH]),
+                AILessonScript.status.in_([STATUS_DRAFT, STATUS_PUBLISH]),
                 AILessonScript.script_id == block_id,
-            ).first()
+            )
+            .order_by(AILessonScript.id.desc())
+            .first()
+        )
         if not block:
             raise_error(""SHIFU.BLOCK_NOT_FOUND"")
-        change_block_status_to_history(block, user_id, datetime.now())
+        mark_block_to_delete(block, user_id, datetime.now())
         db.session.commit()
         return True
     pass
@@ -260,7 +262,6 @@ def save_block_list_internal(
                         new_block.script_index = block_index
                         new_block.lesson_id = current_outline_id
                         change_block_status_to_history(block_model, user_id, time)
-
                         db.session.add(new_block)
                         app.logger.info(
                             f""update block : {new_block.id} {new_block.status}""
@@ -280,7 +281,7 @@ def save_block_list_internal(
         for block in blocks:
             if block.script_id not in save_block_ids:
                 app.logger.info(""delete block : {}"".format(block.script_id))
-                change_block_status_to_history(block, user_id, time)
+                mark_block_to_delete(block, user_id, time)
         db.session.commit()
         return SaveBlockListResultDto(
             [