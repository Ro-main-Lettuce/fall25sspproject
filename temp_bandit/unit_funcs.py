@@ -16,8 +16,6 @@
     SCRIPT_TYPE_SYSTEM,
 )
 from flaskr.service.shifu.const import UNIT_TYPE_TRIAL, UNIT_TYPE_NORMAL
-from sqlalchemy.sql import func, cast
-from sqlalchemy import String
 from flaskr.service.check_risk.funcs import check_text_with_risk_control
 from flaskr.service.shifu.utils import (
     get_existing_outlines,
@@ -87,18 +85,46 @@ def create_unit(
             app.logger.info(
                 f""create unit, user_id: {user_id}, shifu_id: {shifu_id}, parent_id: {parent_id}, unit_index: {unit_index}""
             )
+
+            chapter_units = [
+                unit for unit in existing_outlines if unit.parent_id == parent_id
+            ]
+            chapter_units.sort(key=lambda x: x.lesson_no)
+
+            max_lesson_index = (
+                max([unit.lesson_index for unit in chapter_units])
+                if chapter_units
+                else 0
+            )
+            new_lesson_index = max_lesson_index + 1
+
+            if not chapter_units:
+                unit_no = chapter.lesson_no + ""01""
+            else:
+                if unit_index >= len(chapter_units):
+                    last_unit_no = chapter_units[-1].lesson_no[-2:]
+                    unit_no = chapter.lesson_no + f""{int(last_unit_no) + 1:02d}""
+                else:
+                    next_unit_no = chapter_units[unit_index].lesson_no[-2:]
+                    unit_no = chapter.lesson_no + next_unit_no
+
+                    for unit in chapter_units[unit_index:]:
+                        current_unit_no = unit.lesson_no[-2:]
+                        unit.lesson_no = (
+                            chapter.lesson_no + f""{int(current_unit_no) + 1:02d}""
+                        )
+                        db.session.add(unit)
+
             unit_id = generate_id(app)
-            unit_no = chapter.lesson_no + f""{unit_index + 1:02d}""
             app.logger.info(
-                f""create unit, user_id: {user_id}, shifu_id: {shifu_id}, parent_id: {parent_id}, unit_no: {unit_no} unit_index: {unit_index}""
+                f""create unit, user_id: {user_id}, shifu_id: {shifu_id}, parent_id: {parent_id}, unit_no: {unit_no} unit_index: {new_lesson_index}""
             )
 
             type = LESSON_TYPE_TRIAL
             if unit_type == UNIT_TYPE_NORMAL:
                 type = LESSON_TYPE_NORMAL
             elif unit_type == UNIT_TYPE_TRIAL:
                 type = LESSON_TYPE_TRIAL
-
             if unit_is_hidden:
                 type = LESSON_TYPE_BRANCH_HIDDEN
 
@@ -111,24 +137,11 @@ def create_unit(
                 created_user_id=user_id,
                 updated_user_id=user_id,
                 status=STATUS_DRAFT,
-                lesson_index=unit_index,
+                lesson_index=new_lesson_index,
                 lesson_type=type,
                 parent_id=parent_id,
             )
             check_text_with_risk_control(app, unit_id, user_id, unit.get_str_to_check())
-            AILesson.query.filter(
-                AILesson.course_id == shifu_id,
-                AILesson.status.in_([STATUS_PUBLISH, STATUS_DRAFT]),
-                AILesson.parent_id == parent_id,
-                AILesson.lesson_index >= unit_index,
-                AILesson.lesson_id != unit_id,
-            ).update(
-                {
-                    ""lesson_index"": AILesson.lesson_index + 1,
-                    ""lesson_no"": chapter.lesson_no
-                    + func.lpad(cast(AILesson.lesson_index + 1, String), 2, ""0""),
-                }
-            )
 
             if unit_system_prompt:
                 system_script = AILessonScript.query.filter(