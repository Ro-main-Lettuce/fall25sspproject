@@ -58,7 +58,7 @@ def update_lesson():
               required: false
               schema:
                 type: string
-            - name: app_secrect
+            - name: app_secret
               in: query
               description: 飞书应用秘钥,不传则使用默认的飞书应用秘钥
               required: false
@@ -78,7 +78,7 @@ def update_lesson():
         view_id = request.args.get(""view_id"")
         lesson_type = request.args.get(""lesson_type"", LESSON_TYPE_NORMAL)
         app_id = request.args.get(""app_id"", None)
-        app_secrect = request.args.get(""app_secrect"", None)
+        app_secret = request.args.get(""app_secret"", None)
         course_id = request.args.get(""course_id"", None)
         if not doc_id:
             raise_param_error(""doc_id is not found"")
@@ -98,14 +98,14 @@ def update_lesson():
                 index,
                 lesson_type,
                 app_id,
-                app_secrect,
+                app_secret,
                 course_id,
             )
         )
 
-    @app.route(path_prefix + ""/get_chatper_info"", methods=[""GET""])
+    @app.route(path_prefix + ""/get_chapter_info"", methods=[""GET""])
     @bypass_token_validation
-    def get_chatper_info():
+    def get_chapter_info():
         """"""
         获取课程列表
         ---