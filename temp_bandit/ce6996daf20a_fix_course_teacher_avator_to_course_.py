@@ -27,7 +27,6 @@ def upgrade():
         )
 
 
-
 def downgrade():
     with op.batch_alter_table(""ai_course"", schema=None) as batch_op:
         batch_op.alter_column(