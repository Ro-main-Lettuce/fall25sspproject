@@ -15,6 +15,10 @@
     DISCOUNT_TYPE_FIXED,
     DISCOUNT_TYPE_PERCENT,
 )
+from flaskr.service.lesson.const import (
+    STATUS_PUBLISH,
+    STATUS_DRAFT,
+)
 from flaskr.service.common.dtos import USER_STATE_PAID, USER_STATE_REGISTERED
 from flaskr.service.user.models import User, UserConversion
 from flaskr.service.active import (
@@ -585,16 +589,21 @@ def success_buy_record(app: Flask, record_id: str):
 
 
 def init_trial_lesson(
-    app: Flask, user_id: str, course_id: str
+    app: Flask, user_id: str, course_id: str, preview_mode: bool = False
 ) -> list[AICourseLessonAttendDTO]:
     app.logger.info(
         ""init trial lesson for user:{} course:{}"".format(user_id, course_id)
     )
     response = []
+
+    if preview_mode:
+        status = [STATUS_DRAFT]
+    else:
+        status = [STATUS_PUBLISH]
     lessons = AILesson.query.filter(
         AILesson.course_id == course_id,
         AILesson.lesson_type == LESSON_TYPE_TRIAL,
-        AILesson.status == 1,
+        AILesson.status.in_(status),
     ).all()
     app.logger.info(""init trial lesson:{}"".format(lessons))
     for lesson in lessons: