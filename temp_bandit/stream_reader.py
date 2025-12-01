@@ -6,14 +6,16 @@
 import stat
 import time
 from io import IOBase
-from typing import Dict, Iterable, List, Optional
+from typing import Iterable, List, Optional, Tuple
 
 import psutil
 from typing_extensions import override
 
 from airbyte_cdk import FailureType
+from airbyte_cdk.models import AirbyteRecordMessageFileReference
 from airbyte_cdk.sources.file_based.exceptions import FileSizeLimitError
 from airbyte_cdk.sources.file_based.file_based_stream_reader import AbstractFileBasedStreamReader, FileReadMode
+from airbyte_cdk.sources.file_based.file_record_data import FileRecordData
 from airbyte_cdk.sources.file_based.remote_file import RemoteFile
 from source_sftp_bulk.client import SFTPClient
 from source_sftp_bulk.spec import SourceSFTPBulkSpec
@@ -119,7 +121,9 @@ def progress_handler(bytes_copied, total_bytes):
         return progress_handler
 
     @override
-    def get_file(self, file: RemoteFile, local_directory: str, logger: logging.Logger) -> Dict[str, str | int]:
+    def upload(
+        self, file: RemoteFile, local_directory: str, logger: logging.Logger
+    ) -> Tuple[FileRecordData, AirbyteRecordMessageFileReference]:
         """"""
         Downloads a file from SFTP server to a specified local directory.
 
@@ -129,11 +133,7 @@ def get_file(self, file: RemoteFile, local_directory: str, logger: logging.Logge
             logger (logging.Logger): Logger for logging information and errors.
 
         Returns:
-            dict: A dictionary containing the following:
-                - ""file_url"" (str): The absolute path of the downloaded file.
-                - ""bytes"" (int): The file size in bytes.
-                - ""file_relative_path"" (str): The relative path of the file for local storage. Is relative to local_directory as
-                this a mounted volume in the pod container.
+            Tuple[FileRecordData, AirbyteRecordMessageFileReference]: Contains file record data and file reference for Airbyte protocol.
 
         Raises:
             FileSizeLimitError: If the file size exceeds the predefined limit (1 GB).
@@ -144,7 +144,10 @@ def get_file(self, file: RemoteFile, local_directory: str, logger: logging.Logge
             message = ""File size exceeds the 1 GB limit.""
             raise FileSizeLimitError(message=message, internal_message=message, failure_type=FailureType.config_error)
 
-        file_relative_path, local_file_path, absolute_file_path = self._get_file_transfer_paths(file, local_directory)
+        file_paths = self._get_file_transfer_paths(file.uri, local_directory)
+        local_file_path = file_paths[self.LOCAL_FILE_PATH]
+        file_relative_path = file_paths[self.FILE_RELATIVE_PATH]
+        file_name = file_paths[self.FILE_NAME]
 
         # Get available disk space
         disk_usage = psutil.disk_usage(""/"")
@@ -171,7 +174,21 @@ def get_file(self, file: RemoteFile, local_directory: str, logger: logging.Logge
         logger.info(f""Time taken to download the file {file.uri}: {download_duration:,.2f} seconds."")
         logger.info(f""File {file_relative_path} successfully written to {local_directory}."")
 
-        return {""file_url"": absolute_file_path, ""bytes"": file_size, ""file_relative_path"": file_relative_path}
+        file_record_data = FileRecordData(
+            folder=file_paths[self.FILE_FOLDER],
+            file_name=file_name,
+            bytes=file_size,
+            updated_at=file.last_modified.strftime(""%Y-%m-%dT%H:%M:%S.%fZ""),
+            source_uri=f""sftp://{self.config.username}@{self.config.host}:{self.config.port}{file.uri}"",
+        )
+
+        file_reference = AirbyteRecordMessageFileReference(
+            staging_file_url=local_file_path,
+            source_file_relative_path=file_relative_path,
+            file_size_bytes=file_size,
+        )
+
+        return file_record_data, file_reference
 
     def file_size(self, file: RemoteFile):
         file_size = self.sftp_client.sftp_connection.stat(file.uri).st_size