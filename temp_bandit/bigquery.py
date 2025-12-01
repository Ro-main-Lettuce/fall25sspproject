@@ -287,8 +287,7 @@ def _swap_temp_table_with_final_table(
         deletion_name = f""{final_table_name}_deleteme""
         commands = ""
"".join(
             [
-                f""ALTER TABLE {self._fully_qualified(final_table_name)} ""
-                f""RENAME TO {deletion_name};"",
+                f""ALTER TABLE {self._fully_qualified(final_table_name)} RENAME TO {deletion_name};"",
                 f""ALTER TABLE {self._fully_qualified(temp_table_name)} ""
                 f""RENAME TO {final_table_name};"",
                 f""DROP TABLE {self._fully_qualified(deletion_name)};"",