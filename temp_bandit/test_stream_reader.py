@@ -30,7 +30,13 @@
 
 def create_mock_drive_item(is_file, name, children=None):
     """"""Helper function to create a mock drive item.""""""
-    mock_item = MagicMock(properties={""@microsoft.graph.downloadUrl"": ""test_url"", ""lastModifiedDateTime"": ""1991-08-24""})
+    mock_item = MagicMock(
+        properties={
+            ""@microsoft.graph.downloadUrl"": ""test_url"",
+            ""lastModifiedDateTime"": datetime(1991, 8, 24),
+            ""createdDateTime"": datetime(1991, 8, 24),
+        }
+    )
     mock_item.is_file = is_file
     mock_item.name = name
     mock_item.children.get.return_value.execute_query = Mock(return_value=children or [])
@@ -62,8 +68,18 @@ def create_mock_drive_files():
     Provides mock data for SharePoint drive files (personal drive).
     """"""
     return [
-        (""file1.csv"", ""https://example.com/file1.csv"", datetime(2021, 1, 1)),
-        (""file2.txt"", ""https://example.com/file2.txt"", datetime(2021, 1, 1)),
+        MicrosoftSharePointRemoteFile(
+            uri=""file1.csv"",
+            download_url=""https://example.com/file1.csv"",
+            last_modified=datetime(2021, 1, 1),
+            created_at=datetime(2021, 1, 1),
+        ),
+        MicrosoftSharePointRemoteFile(
+            uri=""file2.txt"",
+            download_url=""https://example.com/file2.txt"",
+            last_modified=datetime(2021, 1, 1),
+            created_at=datetime(2021, 1, 1),
+        ),
     ]
 
 
@@ -73,8 +89,18 @@ def create_mock_shared_drive_files():
     Provides mock data for SharePoint drive files (shared drives).
     """"""
     return [
-        (""file3.csv"", ""https://example.com/file3.csv"", datetime(2021, 3, 1)),
-        (""file4.txt"", ""https://example.com/file4.txt"", datetime(2021, 4, 1)),
+        MicrosoftSharePointRemoteFile(
+            uri=""file3.csv"",
+            download_url=""https://example.com/file3.csv"",
+            last_modified=datetime(2021, 3, 1),
+            created_at=datetime(2021, 3, 1),
+        ),
+        MicrosoftSharePointRemoteFile(
+            uri=""file4.txt"",
+            download_url=""https://example.com/file4.txt"",
+            last_modified=datetime(2021, 4, 1),
+            created_at=datetime(2021, 4, 1),
+        ),
     ]
 
 
@@ -204,32 +230,36 @@ def test_open_file(mock_smart_open, file_extension, expected_compression):
         (
             ""https://my_favorite_sharepoint.sharepoint.com/Shared%20Documents/file"",
             ""txt.gz"",
-            {""bytes"": ANY, ""file_relative_path"": ""file.txt.gz"", ""file_url"": f""{TEST_LOCAL_DIRECTORY}/file.txt.gz""},
+            {""bytes"": ANY, ""source_file_relative_path"": ""file.txt.gz"", ""staging_file_url"": f""{TEST_LOCAL_DIRECTORY}/file.txt.gz""},
         ),
         (
             ""https://my_favorite_sharepoint.sharepoint.com/Shared%20Documents/file"",
             ""txt.bz2"",
-            {""bytes"": ANY, ""file_relative_path"": ""file.txt.bz2"", ""file_url"": f""{TEST_LOCAL_DIRECTORY}/file.txt.bz2""},
+            {""bytes"": ANY, ""source_file_relative_path"": ""file.txt.bz2"", ""staging_file_url"": f""{TEST_LOCAL_DIRECTORY}/file.txt.bz2""},
         ),
         (
             ""https://my_favorite_sharepoint.sharepoint.com/Shared%20Documents/file"",
             ""txt"",
-            {""bytes"": ANY, ""file_relative_path"": ""file.txt"", ""file_url"": f""{TEST_LOCAL_DIRECTORY}/file.txt""},
+            {""bytes"": ANY, ""source_file_relative_path"": ""file.txt"", ""staging_file_url"": f""{TEST_LOCAL_DIRECTORY}/file.txt""},
         ),
         (
             ""https://my_favorite_sharepoint.sharepoint.com/sites/NOT_DEFAULT_SITE/Shared%20Documents/file"",
             ""txt.gz"",
-            {""bytes"": ANY, ""file_relative_path"": ""file.txt.gz"", ""file_url"": f""{TEST_LOCAL_DIRECTORY}/file.txt.gz""},
+            {""bytes"": ANY, ""source_file_relative_path"": ""file.txt.gz"", ""staging_file_url"": f""{TEST_LOCAL_DIRECTORY}/file.txt.gz""},
         ),
         (
             ""https://my_favorite_sharepoint.sharepoint.com/sites/NOT_DEFAULT_SITE/Shared%20Documents/file"",
             ""txt.bz2"",
-            {""bytes"": ANY, ""file_relative_path"": ""file.txt.bz2"", ""file_url"": f""{TEST_LOCAL_DIRECTORY}/file.txt.bz2""},
+            {""bytes"": ANY, ""source_file_relative_path"": ""file.txt.bz2"", ""staging_file_url"": f""{TEST_LOCAL_DIRECTORY}/file.txt.bz2""},
         ),
         (
-            ""https://my_favorite_sharepoint.sharepoint.com/sites/NOT_DEFAULT_SITE/Shared%20Documents/file"",
+            ""https://my_favorite_sharepoint.sharepoint.com/sites/NOT_DEFAULT_SITE/Shared%20Documents/some/path/to/file"",
             ""txt"",
-            {""bytes"": ANY, ""file_relative_path"": ""file.txt"", ""file_url"": f""{TEST_LOCAL_DIRECTORY}/file.txt""},
+            {
+                ""bytes"": ANY,
+                ""source_file_relative_path"": ""some/path/to/file.txt"",
+                ""staging_file_url"": f""{TEST_LOCAL_DIRECTORY}/some/path/to/file.txt"",
+            },
         ),
     ],
 )
@@ -253,6 +283,8 @@ def test_get_file(mock_requests_head, mock_requests_get, mock_get_access_token,
     """"""
     file_uri = f""{file_uri}.{file_extension}""
     mock_file = Mock(download_url=f""https://example.com/file.{file_extension}"", uri=file_uri)
+    mock_file.last_modified = datetime(2021, 1, 1)
+    mock_file.created_at = datetime(2021, 1, 1)
     mock_logger = Mock()
     mock_get_access_token.return_value = ""dummy_access_token""
 
@@ -271,12 +303,22 @@ def test_get_file(mock_requests_head, mock_requests_get, mock_get_access_token,
     stream_reader = SourceMicrosoftSharePointStreamReader()
     stream_reader._config = Mock()  # Assuming _config is required
 
-    result = stream_reader.get_file(mock_file, TEST_LOCAL_DIRECTORY, mock_logger)
+    file_record_data, file_reference = stream_reader.upload(mock_file, TEST_LOCAL_DIRECTORY, mock_logger)
+
+    expected_file_bytes = expected_paths[""bytes""]
+    expected_source_file_relative_path = expected_paths[""source_file_relative_path""]
+    expected_staging_file_url = expected_paths[""staging_file_url""]
+
+    assert file_reference.source_file_relative_path == expected_source_file_relative_path
+    assert file_reference.staging_file_url == expected_staging_file_url
+    assert file_reference.file_size_bytes == expected_file_bytes
 
-    assert result == expected_paths
+    assert os.path.basename(expected_staging_file_url) == file_record_data.file_name
+    assert os.path.dirname(expected_staging_file_url.replace(f""{TEST_LOCAL_DIRECTORY}"", """")) == file_record_data.folder
+    assert file_record_data.source_uri == file_uri
 
     # Check if the file exists at the file_url path
-    assert os.path.exists(result[""file_url""])
+    assert os.path.exists(file_reference.staging_file_url)
 
 
 @patch(""source_microsoft_sharepoint.stream_reader.SourceMicrosoftSharePointStreamReader.get_access_token"")
@@ -296,7 +338,7 @@ def test_get_file_size_error_fetching_metadata_for_missing_header(mock_requests_
     stream_reader = SourceMicrosoftSharePointStreamReader()
     stream_reader._config = Mock()  # Assuming _config is required
     with pytest.raises(ErrorFetchingMetadata, match=""Size was expected in metadata response but was missing""):
-        stream_reader.get_file(mock_file, TEST_LOCAL_DIRECTORY, mock_logger)
+        stream_reader.upload(mock_file, TEST_LOCAL_DIRECTORY, mock_logger)
 
 
 @patch(""source_microsoft_sharepoint.stream_reader.SourceMicrosoftSharePointStreamReader.get_access_token"")
@@ -321,7 +363,7 @@ def test_get_file_size_error_fetching_metadata(mock_requests_head, mock_get_acce
     stream_reader._config = Mock()  # Assuming _config is required
 
     with pytest.raises(ErrorFetchingMetadata, match=""An error occurred while retrieving file size: 500 Server Error""):
-        stream_reader.get_file(mock_file, TEST_LOCAL_DIRECTORY, mock_logger)
+        stream_reader.upload(mock_file, TEST_LOCAL_DIRECTORY, mock_logger)
 
 
 def test_microsoft_sharepoint_client_initialization(requests_mock):
@@ -366,8 +408,20 @@ def test_list_directories_and_files():
 
     assert len(result) == 2
     assert result == [
-        (""https://example.com/root/folder1/file1.txt"", ""test_url"", ""1991-08-24""),
-        (""https://example.com/root/file2.txt"", ""test_url"", ""1991-08-24""),
+        MicrosoftSharePointRemoteFile(
+            uri=""https://example.com/root/folder1/file1.txt"",
+            last_modified=datetime(1991, 8, 24, 0, 0),
+            mime_type=None,
+            download_url=""test_url"",
+            created_at=datetime(1991, 8, 24, 0, 0),
+        ),
+        MicrosoftSharePointRemoteFile(
+            uri=""https://example.com/root/file2.txt"",
+            last_modified=datetime(1991, 8, 24, 0, 0),
+            mime_type=None,
+            download_url=""test_url"",
+            created_at=datetime(1991, 8, 24, 0, 0),
+        ),
     ]
 
 
@@ -465,6 +519,7 @@ def test_get_shared_files_from_all_drives(
     ""name"": ""TestFile.txt"",
     ""@microsoft.graph.downloadUrl"": ""http://example.com/download"",
     ""lastModifiedDateTime"": ""2021-01-01T00:00:00Z"",
+    ""createdDateTime"": ""2021-01-01T00:00:00Z"",
 }
 
 empty_folder_response = {""folder"": True, ""value"": []}
@@ -489,6 +544,7 @@ def test_get_shared_files_from_all_drives(
             ""name"": ""NestedFile.txt"",
             ""@microsoft.graph.downloadUrl"": ""http://example.com/nested"",
             ""lastModifiedDateTime"": ""2021-01-02T00:00:00Z"",
+            ""createdDateTime"": ""2021-01-02T00:00:00Z"",
         }
     ],
     ""name"": ""subfolder2"",
@@ -503,11 +559,13 @@ def test_get_shared_files_from_all_drives(
             file_response,
             [],
             [
-                (
-                    ""http://example.com/TestFile.txt"",
-                    ""http://example.com/download"",
-                    datetime.strptime(""2021-01-01T00:00:00Z"", ""%Y-%m-%dT%H:%M:%SZ""),
-                )
+                MicrosoftSharePointRemoteFile(
+                    uri=""http://example.com/TestFile.txt"",
+                    last_modified=datetime(2021, 1, 1, 0, 0),
+                    mime_type=None,
+                    download_url=""http://example.com/download"",
+                    created_at=datetime(2021, 1, 1, 0, 0),
+                ),
             ],
             False,
             None,
@@ -524,10 +582,12 @@ def test_get_shared_files_from_all_drives(
                 not_empty_subfolder_response,
             ],
             [
-                (
-                    ""http://example.com/subfolder2/NestedFile.txt"",
-                    ""http://example.com/nested"",
-                    datetime.strptime(""2021-01-02T00:00:00Z"", ""%Y-%m-%dT%H:%M:%SZ""),
+                MicrosoftSharePointRemoteFile(
+                    uri=""http://example.com/subfolder2/NestedFile.txt"",
+                    last_modified=datetime(2021, 1, 2, 0, 0),
+                    mime_type=None,
+                    download_url=""http://example.com/nested"",
+                    created_at=datetime(2021, 1, 2, 0, 0),
                 )
             ],
             False,