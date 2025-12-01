@@ -295,7 +295,7 @@ def get_lesson_tree_to_study(
 ) -> AICourseDTO:
     return run_with_redis(
         app,
-        app.config.get(""REDIS_KEY_PRRFIX"") + ""::get_lesson_tree_to_study:"" + user_id,
+        app.config.get(""REDIS_KEY_PREFIX"") + ""::get_lesson_tree_to_study:"" + user_id,
         5,
         get_lesson_tree_to_study_inner,
         [app, user_id, course_id],