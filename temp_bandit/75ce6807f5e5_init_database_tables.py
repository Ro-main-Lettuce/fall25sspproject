@@ -201,7 +201,7 @@ def upgrade():
             comment=""Course feishu ID"",
         ),
         sa.Column(
-            ""course_teacher_avatar"",
+            ""course_teacher_avator"",
             sa.String(length=255),
             nullable=False,
             comment=""Course teacher avatar"",