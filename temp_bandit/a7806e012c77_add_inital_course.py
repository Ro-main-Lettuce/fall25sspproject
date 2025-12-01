@@ -8,6 +8,7 @@
 
 from alembic import op
 import sqlalchemy as sa
+from sqlalchemy import text
 
 # revision identifiers, used by Alembic.
 revision = ""a7806e012c77""
@@ -24,6 +25,13 @@ def upgrade():
                 ""course_keywords"", sa.Text(), nullable=False, comment=""Course keywords""
             )
         )
+        batch_op.alter_column(
+            ""course_teacher_avator"",
+            new_column_name=""course_teacher_avatar"",
+            existing_type=sa.String(length=255),
+            existing_nullable=False,
+            existing_server_default=text(""''""),
+        )
     with op.batch_alter_table(""ai_lesson"", schema=None) as batch_op:
         batch_op.add_column(
             sa.Column(
@@ -102,6 +110,13 @@ def upgrade():
     )
     with op.batch_alter_table(""ai_course"", schema=None) as batch_op:
         batch_op.drop_column(""course_keywords"")
+        batch_op.alter_column(
+            ""course_teacher_avatar"",
+            new_column_name=""course_teacher_avator"",
+            existing_type=sa.String(length=255),
+            existing_nullable=False,
+            existing_server_default=text(""''""),
+        )
     with op.batch_alter_table(""ai_lesson"", schema=None) as batch_op:
         batch_op.drop_column(batch_op.f(""parent_id""))
     with op.batch_alter_table(""ai_lesson_script"", schema=None) as batch_op: