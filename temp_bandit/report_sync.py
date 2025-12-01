@@ -113,24 +113,24 @@ def sync_config_file_to_storage(self, slug: str) -> None:
 
         remote_config_file_path = f""{self.REMOTE_CONFIG_DIR_PREFIX}/{slug}.json""
         self.storage_service.upload_file(str(config_file_path), remote_config_file_path)
-        
+
     def sync_static_files_to_storage(self, slug: str) -> None:
         """"""
         レポートの静的ファイルをストレージにアップロードする
-        
+
         Args:
             slug: レポートのスラッグ
         """"""
         static_dir = settings.REPORT_DIR / slug / ""static""
         if not static_dir.exists():
             logger.warning(f""静的ファイルディレクトリが存在しません: {static_dir}"")
             return
-            
+
         remote_dir_prefix = f""{self.REMOTE_REPORT_DIR_PREFIX}/{slug}/static""
-        
+
         # ファイルをストレージにアップロード
         upload_success = self.storage_service.upload_directory(str(static_dir), remote_dir_prefix)
-        
+
         if upload_success:
             logger.info(f""レポート {slug} の静的ファイルをストレージに同期しました"")
         else: