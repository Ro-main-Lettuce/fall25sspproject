@@ -156,7 +156,7 @@ def _write_files_to_new_table(
                 [{files_list}],
                 format = 'newline_delimited',
                 union_by_name = true,
-                columns = {{ { columns_type_map } }}
+                columns = {{ {columns_type_map} }}
             )
             """"""
         )