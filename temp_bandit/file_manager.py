@@ -106,13 +106,14 @@ def _rename_file(self, new_filename: str) -> None:
         assert self.filename is not None
         self._create_parent_directories(new_filename)
         try:
-            os.rename(self.filename, new_filename)
+            # Use pathlib.Path for cross-platform path handling
+            src_path = pathlib.Path(self.filename)
+            dst_path = pathlib.Path(new_filename)
+            src_path.rename(dst_path)
         except Exception as err:
             raise HTTPException(
                 status_code=HTTPStatus.SERVER_ERROR,
-                detail=""Failed to rename from {0} to {1}"".format(
-                    self.filename, new_filename
-                ),
+                detail=f""Failed to rename from {self.filename} to {new_filename}"",
             ) from err
 
     def _save_file(