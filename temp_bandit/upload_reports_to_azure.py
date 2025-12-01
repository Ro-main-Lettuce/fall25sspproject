@@ -41,7 +41,9 @@
     from azure.storage.blob import BlobServiceClient
 except ImportError as e:
     logger.error(f""Error importing Azure libraries: {e}"")
-    logger.error(""Please install required packages: pip install azure-storage-blob azure-identity"")
+    logger.error(
+        ""Please install required packages: pip install azure-storage-blob azure-identity""
+    )
     sys.exit(1)
 
 
@@ -53,24 +55,30 @@ def __init__(self):
         self.storage_type = os.environ.get(""STORAGE_TYPE"", ""local"")
         self.account_name = os.environ.get(""AZURE_BLOB_STORAGE_ACCOUNT_NAME"", """")
         self.container_name = os.environ.get(""AZURE_BLOB_STORAGE_CONTAINER_NAME"", """")
-        
+
         self.account_url = f""https://{self.account_name}.blob.core.windows.net""
-        
+
         self.blob_service_client = None
         self.container_client = None
 
     def check_environment(self):
         """"""Check if the environment is properly configured for Azure Blob Storage.""""""
         if self.storage_type != ""azure_blob"":
-            logger.error(""STORAGE_TYPE is not set to 'azure_blob'. Please update your .env file."")
+            logger.error(
+                ""STORAGE_TYPE is not set to 'azure_blob'. Please update your .env file.""
+            )
             return False
 
         if not self.account_name:
-            logger.error(""AZURE_BLOB_STORAGE_ACCOUNT_NAME is not set. Please update your .env file."")
+            logger.error(
+                ""AZURE_BLOB_STORAGE_ACCOUNT_NAME is not set. Please update your .env file.""
+            )
             return False
 
         if not self.container_name:
-            logger.error(""AZURE_BLOB_STORAGE_CONTAINER_NAME is not set. Please update your .env file."")
+            logger.error(
+                ""AZURE_BLOB_STORAGE_CONTAINER_NAME is not set. Please update your .env file.""
+            )
             return False
 
         return True
@@ -114,15 +122,19 @@ def upload_file(self, local_file_path, remote_blob_path, skip_if_same=True):
 
             with open(local_file_path, ""rb"") as data:
                 blob_client.upload_blob(data, overwrite=True)
-            logger.info(f""ファイルをアップロードしました。パス: '{local_file_path}' -> '{remote_blob_path}'"")
+            logger.info(
+                f""ファイルをアップロードしました。パス: '{local_file_path}' -> '{remote_blob_path}'""
+            )
             return True
         except Exception as e:
             logger.error(
                 f""ファイルのアップロードに失敗しました。パス: '{local_file_path}' -> '{remote_blob_path}' エラー: {str(e)}""
             )
             return False
 
-    def upload_directory(self, local_dir_path, remote_dir_prefix, target_suffixes=(), skip_if_same=True):
+    def upload_directory(
+        self, local_dir_path, remote_dir_prefix, target_suffixes=(), skip_if_same=True
+    ):
         """"""Upload a directory to Azure Blob Storage.""""""
         try:
             prefix = remote_dir_prefix
@@ -137,18 +149,26 @@ def upload_directory(self, local_dir_path, remote_dir_prefix, target_suffixes=()
                     file_path = os.path.join(root, filename)
                     relative_path = os.path.relpath(file_path, local_dir_path)
                     remote_blob_path = (
-                        prefix + relative_path.replace(os.sep, ""/"") if prefix else relative_path.replace(os.sep, ""/"")
+                        prefix + relative_path.replace(os.sep, ""/"")
+                        if prefix
+                        else relative_path.replace(os.sep, ""/"")
                     )
-                    
-                    if target_suffixes and not any(remote_blob_path.endswith(suffix) for suffix in target_suffixes):
+
+                    if target_suffixes and not any(
+                        remote_blob_path.endswith(suffix) for suffix in target_suffixes
+                    ):
                         continue
 
                     files_processed += 1
-                    success = self.upload_file(file_path, remote_blob_path, skip_if_same=skip_if_same)
+                    success = self.upload_file(
+                        file_path, remote_blob_path, skip_if_same=skip_if_same
+                    )
                     upload_results.append(success)
 
             if files_processed == 0:
-                logger.warning(f""アップロード対象のファイルが見つかりませんでした。パス: '{local_dir_path}'"")
+                logger.warning(
+                    f""アップロード対象のファイルが見つかりませんでした。パス: '{local_dir_path}'""
+                )
                 return False
 
             if not all(upload_results):
@@ -174,10 +194,10 @@ def check_environment():
 def upload_reports(test_mode=False):
     """"""Upload all local reports to Azure Blob Storage.""""""
     uploader = AzureBlobUploader()
-    
+
     if not uploader.check_environment():
         return False
-    
+
     if not test_mode and not uploader.connect():
         return False
 
@@ -211,36 +231,34 @@ def upload_reports(test_mode=False):
     status_upload_success = uploader.upload_file(
         str(STATUS_FILE), ""status/report_status.json""
     )
-    
+
     if not status_upload_success:
         logger.error(""Failed to upload status file."")
         return False
-    
+
     logger.info(""Status file uploaded successfully."")
 
     success_count = 0
     total_count = 0
-    
+
     for slug in status_data:
         total_count += 1
         report_dir = OUTPUT_DIR / slug
-        
+
         if not report_dir.exists():
             logger.warning(f""Report directory not found for slug: {slug}"")
             continue
-        
+
         logger.info(f""Uploading report: {slug}"")
-        
-        upload_success = uploader.upload_directory(
-            str(report_dir), f""outputs/{slug}""
-        )
-        
+
+        upload_success = uploader.upload_directory(str(report_dir), f""outputs/{slug}"")
+
         if upload_success:
             success_count += 1
             logger.info(f""Successfully uploaded report: {slug}"")
         else:
             logger.error(f""Failed to upload report: {slug}"")
-    
+
     logger.info(f""Uploaded {success_count} out of {total_count} reports."")
     return success_count > 0
 
@@ -251,12 +269,14 @@ def main():
         description=""Upload local reports to Azure Blob Storage""
     )
     parser.add_argument(
-        ""--test"", action=""store_true"", help=""Run in test mode (don't actually upload files)""
+        ""--test"",
+        action=""store_true"",
+        help=""Run in test mode (don't actually upload files)"",
     )
     args = parser.parse_args()
 
     logger.info(""Starting upload of reports to Azure Blob Storage..."")
-    
+
     if upload_reports(args.test):
         logger.info(""Upload completed successfully."")
         return 0