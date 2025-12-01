@@ -4,6 +4,7 @@
 
 
 import datetime
+from os import path
 from typing import Dict
 from unittest.mock import ANY, MagicMock, call, patch
 
@@ -41,14 +42,29 @@ def flatten_list(list_of_lists):
     [
         pytest.param(
             ""*"",
-            [[{""files"": [{""id"": ""abc"", ""mimeType"": ""text/csv"", ""name"": ""test.csv"", ""modifiedTime"": ""2021-01-01T00:00:00.000Z""}]}]],
+            [
+                [
+                    {
+                        ""files"": [
+                            {
+                                ""id"": ""abc"",
+                                ""mimeType"": ""text/csv"",
+                                ""name"": ""test.csv"",
+                                ""modifiedTime"": ""2021-01-01T00:00:00.000Z"",
+                                ""webViewLink"": ""https://docs.google.com/file/d/abc/view?usp=drivesdk"",
+                            }
+                        ]
+                    }
+                ]
+            ],
             [
                 GoogleDriveRemoteFile(
                     uri=""test.csv"",
                     id=""abc"",
                     mime_type=""text/csv"",
                     original_mime_type=""text/csv"",
                     last_modified=datetime.datetime(2021, 1, 1),
+                    view_link=f""https://docs.google.com/file/d/abc/view?usp=drivesdk"",
                 )
             ],
             id=""Single file"",
@@ -59,8 +75,20 @@ def flatten_list(list_of_lists):
                 [
                     {
                         ""files"": [
-                            {""id"": ""abc"", ""mimeType"": ""text/csv"", ""name"": ""test.csv"", ""modifiedTime"": ""2021-01-01T00:00:00.000Z""},
-                            {""id"": ""def"", ""mimeType"": ""text/csv"", ""name"": ""another_file.csv"", ""modifiedTime"": ""2021-01-01T00:00:00.000Z""},
+                            {
+                                ""id"": ""abc"",
+                                ""mimeType"": ""text/csv"",
+                                ""name"": ""test.csv"",
+                                ""modifiedTime"": ""2021-01-01T00:00:00.000Z"",
+                                ""webViewLink"": ""https://docs.google.com/file/d/abc/view?usp=drivesdk"",
+                            },
+                            {
+                                ""id"": ""def"",
+                                ""mimeType"": ""text/csv"",
+                                ""name"": ""another_file.csv"",
+                                ""modifiedTime"": ""2021-01-01T00:00:00.000Z"",
+                                ""webViewLink"": ""https://docs.google.com/file/d/def/view?usp=drivesdk"",
+                            },
                         ]
                     },
                 ]
@@ -72,13 +100,15 @@ def flatten_list(list_of_lists):
                     mime_type=""text/csv"",
                     original_mime_type=""text/csv"",
                     last_modified=datetime.datetime(2021, 1, 1),
+                    view_link=f""https://docs.google.com/file/d/abc/view?usp=drivesdk"",
                 ),
                 GoogleDriveRemoteFile(
                     uri=""another_file.csv"",
                     id=""def"",
                     mime_type=""text/csv"",
                     original_mime_type=""text/csv"",
                     last_modified=datetime.datetime(2021, 1, 1),
+                    view_link=f""https://docs.google.com/file/d/def/view?usp=drivesdk"",
                 ),
             ],
             id=""Multiple files"",
@@ -87,10 +117,26 @@ def flatten_list(list_of_lists):
             ""*"",
             [
                 [
-                    {""files"": [{""id"": ""abc"", ""mimeType"": ""text/csv"", ""name"": ""test.csv"", ""modifiedTime"": ""2021-01-01T00:00:00.000Z""}]},
                     {
                         ""files"": [
-                            {""id"": ""def"", ""mimeType"": ""text/csv"", ""name"": ""another_file.csv"", ""modifiedTime"": ""2021-01-01T00:00:00.000Z""}
+                            {
+                                ""id"": ""abc"",
+                                ""mimeType"": ""text/csv"",
+                                ""name"": ""test.csv"",
+                                ""modifiedTime"": ""2021-01-01T00:00:00.000Z"",
+                                ""webViewLink"": ""https://docs.google.com/file/d/abc/view?usp=drivesdk"",
+                            }
+                        ]
+                    },
+                    {
+                        ""files"": [
+                            {
+                                ""id"": ""def"",
+                                ""mimeType"": ""text/csv"",
+                                ""name"": ""another_file.csv"",
+                                ""modifiedTime"": ""2021-01-01T00:00:00.000Z"",
+                                ""webViewLink"": ""https://docs.google.com/file/d/def/view?usp=drivesdk"",
+                            }
                         ]
                     },
                 ]
@@ -102,13 +148,15 @@ def flatten_list(list_of_lists):
                     mime_type=""text/csv"",
                     original_mime_type=""text/csv"",
                     last_modified=datetime.datetime(2021, 1, 1),
+                    view_link=f""https://docs.google.com/file/d/abc/view?usp=drivesdk"",
                 ),
                 GoogleDriveRemoteFile(
                     uri=""another_file.csv"",
                     id=""def"",
                     mime_type=""text/csv"",
                     original_mime_type=""text/csv"",
                     last_modified=datetime.datetime(2021, 1, 1),
+                    view_link=f""https://docs.google.com/file/d/def/view?usp=drivesdk"",
                 ),
             ],
             id=""Multiple pages"",
@@ -129,12 +177,19 @@ def flatten_list(list_of_lists):
                 [
                     {
                         ""files"": [
-                            {""id"": ""abc"", ""mimeType"": ""text/csv"", ""name"": ""test.csv"", ""modifiedTime"": ""2021-01-01T00:00:00.000Z""},
+                            {
+                                ""id"": ""abc"",
+                                ""mimeType"": ""text/csv"",
+                                ""name"": ""test.csv"",
+                                ""modifiedTime"": ""2021-01-01T00:00:00.000Z"",
+                                ""webViewLink"": ""https://docs.google.com/file/d/abc/view?usp=drivesdk"",
+                            },
                             {
                                 ""id"": ""sub"",
                                 ""mimeType"": ""application/vnd.google-apps.folder"",
                                 ""name"": ""subfolder"",
                                 ""modifiedTime"": ""2021-01-01T00:00:00.000Z"",
+                                ""webViewLink"": ""https://docs.google.com/file/d/sub/view?usp=drivesdk"",
                             },
                         ]
                     },
@@ -143,12 +198,19 @@ def flatten_list(list_of_lists):
                     # second request is for requesting the subfolder
                     {
                         ""files"": [
-                            {""id"": ""def"", ""mimeType"": ""text/csv"", ""name"": ""another_file.csv"", ""modifiedTime"": ""2021-01-01T00:00:00.000Z""},
+                            {
+                                ""id"": ""def"",
+                                ""mimeType"": ""text/csv"",
+                                ""name"": ""another_file.csv"",
+                                ""modifiedTime"": ""2021-01-01T00:00:00.000Z"",
+                                ""webViewLink"": ""https://docs.google.com/file/d/def/view?usp=drivesdk"",
+                            },
                             {
                                 ""id"": ""subsub"",
                                 ""mimeType"": ""application/vnd.google-apps.folder"",
                                 ""name"": ""subsubfolder"",
                                 ""modifiedTime"": ""2021-01-01T00:00:00.000Z"",
+                                ""webViewLink"": ""https://docs.google.com/file/d/subsub/view?usp=drivesdk"",
                             },
                         ]
                     },
@@ -162,6 +224,7 @@ def flatten_list(list_of_lists):
                                 ""mimeType"": ""text/csv"",
                                 ""name"": ""yet_another_file.csv"",
                                 ""modifiedTime"": ""2021-01-01T00:00:00.000Z"",
+                                ""webViewLink"": ""https://docs.google.com/file/d/ghi/view?usp=drivesdk"",
                             },
                         ]
                     },
@@ -174,20 +237,23 @@ def flatten_list(list_of_lists):
                     mime_type=""text/csv"",
                     original_mime_type=""text/csv"",
                     last_modified=datetime.datetime(2021, 1, 1),
+                    view_link=f""https://docs.google.com/file/d/abc/view?usp=drivesdk"",
                 ),
                 GoogleDriveRemoteFile(
                     uri=""subfolder/another_file.csv"",
                     id=""def"",
                     mime_type=""text/csv"",
                     original_mime_type=""text/csv"",
                     last_modified=datetime.datetime(2021, 1, 1),
+                    view_link=f""https://docs.google.com/file/d/def/view?usp=drivesdk"",
                 ),
                 GoogleDriveRemoteFile(
                     uri=""subfolder/subsubfolder/yet_another_file.csv"",
                     id=""ghi"",
                     mime_type=""text/csv"",
                     original_mime_type=""text/csv"",
                     last_modified=datetime.datetime(2021, 1, 1),
+                    view_link=f""https://docs.google.com/file/d/ghi/view?usp=drivesdk"",
                 ),
             ],
             id=""Nested directories"",
@@ -198,12 +264,19 @@ def flatten_list(list_of_lists):
                 [
                     {
                         ""files"": [
-                            {""id"": ""abc"", ""mimeType"": ""text/csv"", ""name"": ""test.csv"", ""modifiedTime"": ""2021-01-01T00:00:00.000Z""},
+                            {
+                                ""id"": ""abc"",
+                                ""mimeType"": ""text/csv"",
+                                ""name"": ""test.csv"",
+                                ""modifiedTime"": ""2021-01-01T00:00:00.000Z"",
+                                ""webViewLink"": ""https://docs.google.com/file/d/abc/view?usp=drivesdk"",
+                            },
                             {
                                 ""id"": ""sub"",
                                 ""mimeType"": ""application/vnd.google-apps.folder"",
                                 ""name"": ""subfolder"",
                                 ""modifiedTime"": ""2021-01-01T00:00:00.000Z"",
+                                ""webViewLink"": ""https://docs.google.com/file/d/sub/view?usp=drivesdk"",
                             },
                         ]
                     },
@@ -212,12 +285,19 @@ def flatten_list(list_of_lists):
                     # second request is for requesting the subfolder
                     {
                         ""files"": [
-                            {""id"": ""abc"", ""mimeType"": ""text/csv"", ""name"": ""test.csv"", ""modifiedTime"": ""2021-01-01T00:00:00.000Z""},
+                            {
+                                ""id"": ""abc"",
+                                ""mimeType"": ""text/csv"",
+                                ""name"": ""test.csv"",
+                                ""modifiedTime"": ""2021-01-01T00:00:00.000Z"",
+                                ""webViewLink"": ""https://docs.google.com/file/d/abc/view?usp=drivesdk"",
+                            },
                             {
                                 ""id"": ""subsub"",
                                 ""mimeType"": ""application/vnd.google-apps.folder"",
                                 ""name"": ""subsubfolder"",
                                 ""modifiedTime"": ""2021-01-01T00:00:00.000Z"",
+                                ""webViewLink"": ""https://docs.google.com/file/d/subsub/view?usp=drivesdk"",
                             },
                         ]
                     },
@@ -226,12 +306,19 @@ def flatten_list(list_of_lists):
                     # third request is for requesting the subsubfolder
                     {
                         ""files"": [
-                            {""id"": ""abc"", ""mimeType"": ""text/csv"", ""name"": ""test.csv"", ""modifiedTime"": ""2021-01-01T00:00:00.000Z""},
+                            {
+                                ""id"": ""abc"",
+                                ""mimeType"": ""text/csv"",
+                                ""name"": ""test.csv"",
+                                ""modifiedTime"": ""2021-01-01T00:00:00.000Z"",
+                                ""webViewLink"": ""https://docs.google.com/file/d/abc/view?usp=drivesdk"",
+                            },
                             {
                                 ""id"": ""sub"",
                                 ""mimeType"": ""application/vnd.google-apps.folder"",
                                 ""name"": ""link_to_subfolder"",
                                 ""modifiedTime"": ""2021-01-01T00:00:00.000Z"",
+                                ""webViewLink"": ""https://docs.google.com/file/d/sub/view?usp=drivesdk"",
                             },
                         ]
                     },
@@ -244,6 +331,7 @@ def flatten_list(list_of_lists):
                     mime_type=""text/csv"",
                     original_mime_type=""text/csv"",
                     last_modified=datetime.datetime(2021, 1, 1),
+                    view_link=f""https://docs.google.com/file/d/abc/view?usp=drivesdk"",
                 ),
             ],
             id=""Duplicates"",
@@ -254,12 +342,19 @@ def flatten_list(list_of_lists):
                 [
                     {
                         ""files"": [
-                            {""id"": ""abc"", ""mimeType"": ""text/csv"", ""name"": ""test.csv"", ""modifiedTime"": ""2021-01-01T00:00:00.000Z""},
+                            {
+                                ""id"": ""abc"",
+                                ""mimeType"": ""text/csv"",
+                                ""name"": ""test.csv"",
+                                ""modifiedTime"": ""2021-01-01T00:00:00.000Z"",
+                                ""webViewLink"": ""https://docs.google.com/file/d/abc/view?usp=drivesdk"",
+                            },
                             {
                                 ""id"": ""sub"",
                                 ""mimeType"": ""application/vnd.google-apps.folder"",
                                 ""name"": ""subfolder"",
                                 ""modifiedTime"": ""2021-01-01T00:00:00.000Z"",
+                                ""webViewLink"": ""https://docs.google.com/file/d/sub/view?usp=drivesdk"",
                             },
                         ]
                     },
@@ -268,12 +363,19 @@ def flatten_list(list_of_lists):
                     # second request is for requesting the subfolder
                     {
                         ""files"": [
-                            {""id"": ""def"", ""mimeType"": ""text/csv"", ""name"": ""another_file.csv"", ""modifiedTime"": ""2021-01-01T00:00:00.000Z""},
+                            {
+                                ""id"": ""def"",
+                                ""mimeType"": ""text/csv"",
+                                ""name"": ""another_file.csv"",
+                                ""modifiedTime"": ""2021-01-01T00:00:00.000Z"",
+                                ""webViewLink"": ""https://docs.google.com/file/d/def/view?usp=drivesdk"",
+                            },
                             {
                                 ""id"": ""ghi"",
                                 ""mimeType"": ""text/jsonl"",
                                 ""name"": ""non_matching.jsonl"",
                                 ""modifiedTime"": ""2021-01-01T00:00:00.000Z"",
+                                ""webViewLink"": ""https://docs.google.com/file/d/ghi/view?usp=drivesdk"",
                             },
                         ]
                     },
@@ -286,6 +388,7 @@ def flatten_list(list_of_lists):
                     mime_type=""text/csv"",
                     original_mime_type=""text/csv"",
                     last_modified=datetime.datetime(2021, 1, 1),
+                    view_link=f""https://docs.google.com/file/d/def/view?usp=drivesdk"",
                 ),
             ],
             id=""Glob matching and subdirectories"",
@@ -296,19 +399,27 @@ def flatten_list(list_of_lists):
                 [
                     {
                         ""files"": [
-                            {""id"": ""abc"", ""mimeType"": ""text/csv"", ""name"": ""test.csv"", ""modifiedTime"": ""2021-01-01T00:00:00.000Z""},
+                            {
+                                ""id"": ""abc"",
+                                ""mimeType"": ""text/csv"",
+                                ""name"": ""test.csv"",
+                                ""modifiedTime"": ""2021-01-01T00:00:00.000Z"",
+                                ""webViewLink"": ""https://docs.google.com/file/d/abc/view?usp=drivesdk"",
+                            },
                             {
                                 ""id"": ""sub"",
                                 ""mimeType"": ""application/vnd.google-apps.folder"",
                                 ""name"": ""subfolder"",
                                 ""modifiedTime"": ""2021-01-01T00:00:00.000Z"",
+                                ""webViewLink"": ""https://docs.google.com/file/d/sub/view?usp=drivesdk"",
                             },
                             # This won't get queued because it has no chance of matching the glob
                             {
                                 ""id"": ""sub"",
                                 ""mimeType"": ""application/vnd.google-apps.folder"",
                                 ""name"": ""ignored_subfolder"",
                                 ""modifiedTime"": ""2021-01-01T00:00:00.000Z"",
+                                ""webViewLink"": ""https://docs.google.com/file/d/sub/view?usp=drivesdk"",
                             },
                         ]
                     },
@@ -317,13 +428,20 @@ def flatten_list(list_of_lists):
                     # second request is for requesting the subfolder
                     {
                         ""files"": [
-                            {""id"": ""def"", ""mimeType"": ""text/csv"", ""name"": ""another_file.csv"", ""modifiedTime"": ""2021-01-01T00:00:00.000Z""},
+                            {
+                                ""id"": ""def"",
+                                ""mimeType"": ""text/csv"",
+                                ""name"": ""another_file.csv"",
+                                ""modifiedTime"": ""2021-01-01T00:00:00.000Z"",
+                                ""webViewLink"": ""https://docs.google.com/file/d/def/view?usp=drivesdk"",
+                            },
                             # This will get queued because it matches the prefix (event though it can't match the glob)
                             {
                                 ""id"": ""subsub"",
                                 ""mimeType"": ""application/vnd.google-apps.folder"",
                                 ""name"": ""subsubfolder"",
                                 ""modifiedTime"": ""2021-01-01T00:00:00.000Z"",
+                                ""webViewLink"": ""https://docs.google.com/file/d/subsub/view?usp=drivesdk"",
                             },
                         ]
                     },
@@ -337,6 +455,7 @@ def flatten_list(list_of_lists):
                                 ""mimeType"": ""text/csv"",
                                 ""name"": ""yet_another_file.csv"",
                                 ""modifiedTime"": ""2021-01-01T00:00:00.000Z"",
+                                ""webViewLink"": ""https://docs.google.com/file/d/ghi/view?usp=drivesdk"",
                             },
                         ]
                     },
@@ -349,6 +468,7 @@ def flatten_list(list_of_lists):
                     mime_type=""text/csv"",
                     original_mime_type=""text/csv"",
                     last_modified=datetime.datetime(2021, 1, 1),
+                    view_link=f""https://docs.google.com/file/d/def/view?usp=drivesdk"",
                 ),
             ],
             id=""Glob matching and ignoring most subdirectories that can't be matched"",
@@ -359,12 +479,19 @@ def flatten_list(list_of_lists):
                 [
                     {
                         ""files"": [
-                            {""id"": ""abc"", ""mimeType"": ""text/csv"", ""name"": ""test.csv"", ""modifiedTime"": ""2021-01-01T00:00:00.000Z""},
+                            {
+                                ""id"": ""abc"",
+                                ""mimeType"": ""text/csv"",
+                                ""name"": ""test.csv"",
+                                ""modifiedTime"": ""2021-01-01T00:00:00.000Z"",
+                                ""webViewLink"": ""https://docs.google.com/file/d/abc/view?usp=drivesdk"",
+                            },
                             {
                                 ""id"": ""sub"",
                                 ""mimeType"": ""application/vnd.google-apps.folder"",
                                 ""name"": ""subfolder"",
                                 ""modifiedTime"": ""2021-01-01T00:00:00.000Z"",
+                                ""webViewLink"": ""https://docs.google.com/file/d/sub/view?usp=drivesdk"",
                             },
                         ]
                     },
@@ -373,13 +500,20 @@ def flatten_list(list_of_lists):
                     # second request is for requesting the subfolder
                     {
                         ""files"": [
-                            {""id"": ""def"", ""mimeType"": ""text/csv"", ""name"": ""another_file.csv"", ""modifiedTime"": ""2021-01-01T00:00:00.000Z""},
+                            {
+                                ""id"": ""def"",
+                                ""mimeType"": ""text/csv"",
+                                ""name"": ""another_file.csv"",
+                                ""modifiedTime"": ""2021-01-01T00:00:00.000Z"",
+                                ""webViewLink"": ""https://docs.google.com/file/d/def/view?usp=drivesdk"",
+                            },
                             # This will get queued because it matches the prefix (event though it can't match the glob)
                             {
                                 ""id"": ""subsub"",
                                 ""mimeType"": ""application/vnd.google-apps.folder"",
                                 ""name"": ""subsubfolder"",
                                 ""modifiedTime"": ""2021-01-01T00:00:00.000Z"",
+                                ""webViewLink"": ""https://docs.google.com/file/d/subsub/view?usp=drivesdk"",
                             },
                         ]
                     },
@@ -393,13 +527,15 @@ def flatten_list(list_of_lists):
                                 ""mimeType"": ""text/csv"",
                                 ""name"": ""yet_another_file.csv"",
                                 ""modifiedTime"": ""2021-01-01T00:00:00.000Z"",
+                                ""webViewLink"": ""https://docs.google.com/file/d/ghi/view?usp=drivesdk"",
                             },
                             # This will get queued because it matches the prefix (event though it can't match the glob)
                             {
                                 ""id"": ""subsubsub"",
                                 ""mimeType"": ""application/vnd.google-apps.folder"",
                                 ""name"": ""ignored_subsubsubfolder"",
                                 ""modifiedTime"": ""2021-01-01T00:00:00.000Z"",
+                                ""webViewLink"": ""https://docs.google.com/file/d/subsubsub/view?usp=drivesdk"",
                             },
                         ]
                     },
@@ -413,6 +549,7 @@ def flatten_list(list_of_lists):
                     mime_type=""text/csv"",
                     original_mime_type=""text/csv"",
                     last_modified=datetime.datetime(2021, 1, 1),
+                    view_link=f""https://docs.google.com/file/d/ghi/view?usp=drivesdk"",
                 ),
             ],
             id=""Glob matching and ignoring subdirectories that can't be matched, multiple levels"",
@@ -428,6 +565,7 @@ def flatten_list(list_of_lists):
                                 ""mimeType"": ""application/vnd.google-apps.document"",
                                 ""name"": ""MyDoc"",
                                 ""modifiedTime"": ""2021-01-01T00:00:00.000Z"",
+                                ""webViewLink"": ""https://docs.google.com/document/d/abc/edit?usp=drivesdk"",
                             }
                         ]
                     }
@@ -440,6 +578,7 @@ def flatten_list(list_of_lists):
                     original_mime_type=""application/vnd.google-apps.document"",
                     mime_type=""application/vnd.openxmlformats-officedocument.wordprocessingml.document"",
                     last_modified=datetime.datetime(2021, 1, 1),
+                    view_link=f""https://docs.google.com/document/d/abc/edit?usp=drivesdk"",
                 )
             ],
             id=""Google Doc as docx"",
@@ -455,6 +594,7 @@ def flatten_list(list_of_lists):
                                 ""mimeType"": ""application/vnd.google-apps.presentation"",
                                 ""name"": ""MySlides"",
                                 ""modifiedTime"": ""2021-01-01T00:00:00.000Z"",
+                                ""webViewLink"": ""https://docs.google.com/presentation/d/abc/edit?usp=drivesdk"",
                             }
                         ]
                     }
@@ -467,6 +607,7 @@ def flatten_list(list_of_lists):
                     original_mime_type=""application/vnd.google-apps.presentation"",
                     mime_type=""application/pdf"",
                     last_modified=datetime.datetime(2021, 1, 1),
+                    view_link=f""https://docs.google.com/presentation/d/abc/edit?usp=drivesdk"",
                 )
             ],
             id=""Presentation as pdf"",
@@ -482,6 +623,7 @@ def flatten_list(list_of_lists):
                                 ""mimeType"": ""application/vnd.google-apps.drawing"",
                                 ""name"": ""MyDrawing"",
                                 ""modifiedTime"": ""2021-01-01T00:00:00.000Z"",
+                                ""webViewLink"": ""https://docs.google.com/drawings/d/abc/edit?usp=drivesdk"",
                             }
                         ]
                     }
@@ -494,6 +636,7 @@ def flatten_list(list_of_lists):
                     original_mime_type=""application/vnd.google-apps.drawing"",
                     mime_type=""application/pdf"",
                     last_modified=datetime.datetime(2021, 1, 1),
+                    view_link=f""https://docs.google.com/drawings/d/abc/edit?usp=drivesdk"",
                 )
             ],
             id=""Drawing as pdf"",
@@ -509,6 +652,7 @@ def flatten_list(list_of_lists):
                                 ""mimeType"": ""application/vnd.google-apps.video"",
                                 ""name"": ""MyVideo"",
                                 ""modifiedTime"": ""2021-01-01T00:00:00.000Z"",
+                                ""webViewLink"": ""https://docs.google.com/file/d/abc/view?usp=drivesdk"",
                             }
                         ]
                     }
@@ -521,6 +665,7 @@ def flatten_list(list_of_lists):
                     original_mime_type=""application/vnd.google-apps.video"",
                     mime_type=""application/vnd.google-apps.video"",
                     last_modified=datetime.datetime(2021, 1, 1),
+                    view_link=f""https://docs.google.com/file/d/abc/view?usp=drivesdk"",
                 )
             ],
             id=""Other google file types as is"",
@@ -558,7 +703,12 @@ def test_matching_files(mock_build_service, mock_service_account, glob, listing_
     [
         pytest.param(
             GoogleDriveRemoteFile(
-                uri=""avro_file"", id=""abc"", mime_type=""text/csv"", original_mime_type=""text/csv"", last_modified=datetime.datetime(2021, 1, 1)
+                uri=""avro_file"",
+                id=""abc"",
+                mime_type=""text/csv"",
+                original_mime_type=""text/csv"",
+                last_modified=datetime.datetime(2021, 1, 1),
+                view_link=f""https://docs.google.com/file/d/abc/view?usp=drivesdk"",
             ),
             b""test"",
             FileReadMode.READ_BINARY,
@@ -570,7 +720,12 @@ def test_matching_files(mock_build_service, mock_service_account, glob, listing_
         ),
         pytest.param(
             GoogleDriveRemoteFile(
-                uri=""test.csv"", id=""abc"", mime_type=""text/csv"", original_mime_type=""text/csv"", last_modified=datetime.datetime(2021, 1, 1)
+                uri=""test.csv"",
+                id=""abc"",
+                mime_type=""text/csv"",
+                original_mime_type=""text/csv"",
+                last_modified=datetime.datetime(2021, 1, 1),
+                view_link=f""https://docs.google.com/file/d/abc/view?usp=drivesdk"",
             ),
             b""test"",
             FileReadMode.READ,
@@ -587,6 +742,7 @@ def test_matching_files(mock_build_service, mock_service_account, glob, listing_
                 mime_type=""application/vnd.openxmlformats-officedocument.wordprocessingml.document"",
                 original_mime_type=""application/vnd.google-apps.document"",
                 last_modified=datetime.datetime(2021, 1, 1),
+                view_link=f""https://docs.google.com/document/d/abc/edit?usp=drivesdk"",
             ),
             b""test"",
             FileReadMode.READ_BINARY,
@@ -654,16 +810,21 @@ def mock_next_chunk():
     [
         pytest.param(
             GoogleDriveRemoteFile(
-                uri=""test.jsonl"",
+                uri=""some/path/in/source/test.jsonl"",
                 last_modified=datetime.datetime(2023, 10, 16, 6, 16, 6),
                 mime_type=""application/octet-stream"",
                 id=""1"",
                 original_mime_type=""application/octet-stream"",
+                view_link=f""https://docs.google.com/file/d/1/view?usp=drivesdk"",
             ),
             b""test"",
             False,
             None,
-            {""file_url"": f""{TEST_LOCAL_DIRECTORY}/test.jsonl"", ""bytes"": ANY, ""file_relative_path"": ""test.jsonl""},
+            {
+                ""staging_file_url"": f""{TEST_LOCAL_DIRECTORY}/some/path/in/source/test.jsonl"",
+                ""bytes"": ANY,
+                ""file_relative_path"": ""some/path/in/source/test.jsonl"",
+            },
             False,
             id=""Get jsonl"",
         ),
@@ -674,11 +835,16 @@ def mock_next_chunk():
                 mime_type=""application/octet-stream"",
                 id=""test2"",
                 original_mime_type=""application/octet-stream"",
+                view_link=f""https://docs.google.com/file/d/test2/view?usp=drivesdk"",
             ),
             b""test"",
             False,
             None,
-            {""file_url"": f""{TEST_LOCAL_DIRECTORY}/subfolder/test2.jsonl"", ""bytes"": ANY, ""file_relative_path"": ""subfolder/test2.jsonl""},
+            {
+                ""staging_file_url"": f""{TEST_LOCAL_DIRECTORY}/subfolder/test2.jsonl"",
+                ""bytes"": ANY,
+                ""file_relative_path"": ""subfolder/test2.jsonl"",
+            },
             False,
             id=""Get json2l"",
         ),
@@ -689,11 +855,12 @@ def mock_next_chunk():
                 mime_type=""application/vnd.openxmlformats-officedocument.wordprocessingml.document"",
                 id=""testdoc_docx"",
                 original_mime_type=""application/vnd.openxmlformats-officedocument.wordprocessingml.document"",
+                view_link=f""https://docs.google.com/file/d/testdoc_docx/view?usp=drivesdk"",
             ),
             b""test"",
             False,
             None,
-            {""file_url"": f""{TEST_LOCAL_DIRECTORY}/testdoc_docx.docx"", ""bytes"": ANY, ""file_relative_path"": ""testdoc_docx.docx""},
+            {""staging_file_url"": f""{TEST_LOCAL_DIRECTORY}/testdoc_docx.docx"", ""bytes"": ANY, ""file_relative_path"": ""testdoc_docx.docx""},
             False,
             id=""Get testdoc_docx"",
         ),
@@ -704,11 +871,12 @@ def mock_next_chunk():
                 mime_type=""application/pdf"",
                 id=""testdoc_pdf"",
                 original_mime_type=""application/pdf"",
+                view_link=f""https://docs.google.com/file/d/testdoc_pdf/view?usp=drivesdk"",
             ),
             b""test"",
             False,
             None,
-            {""file_url"": f""{TEST_LOCAL_DIRECTORY}/testdoc_pdf.pdf"", ""bytes"": ANY, ""file_relative_path"": ""testdoc_pdf.pdf""},
+            {""staging_file_url"": f""{TEST_LOCAL_DIRECTORY}/testdoc_pdf.pdf"", ""bytes"": ANY, ""file_relative_path"": ""testdoc_pdf.pdf""},
             False,
             id=""Read testdoc_pdf"",
         ),
@@ -719,11 +887,12 @@ def mock_next_chunk():
                 mime_type=""application/pdf"",
                 id=""testdoc_ocr_pdf"",
                 original_mime_type=""application/pdf"",
+                view_link=f""https://docs.google.com/file/d/testdoc_ocr_pdf/view?usp=drivesdk"",
             ),
             b""test"",
             False,
             None,
-            {""file_url"": f""{TEST_LOCAL_DIRECTORY}/testdoc_ocr_pdf.pdf"", ""bytes"": ANY, ""file_relative_path"": ""testdoc_ocr_pdf.pdf""},
+            {""staging_file_url"": f""{TEST_LOCAL_DIRECTORY}/testdoc_ocr_pdf.pdf"", ""bytes"": ANY, ""file_relative_path"": ""testdoc_ocr_pdf.pdf""},
             False,
             id=""Read testdoc_ocr_pdf"",
         ),
@@ -734,11 +903,12 @@ def mock_next_chunk():
                 mime_type=""application/vnd.openxmlformats-officedocument.wordprocessingml.document"",
                 id=""testdoc_google"",
                 original_mime_type=""application/vnd.google-apps.document"",
+                view_link=f""https://docs.google.com/document/d/testdoc_google/edit?usp=drivesdk"",
             ),
             b""test"",
             True,
             ""application/vnd.openxmlformats-officedocument.wordprocessingml.document"",
-            {""file_url"": f""{TEST_LOCAL_DIRECTORY}/testdoc_google.docx"", ""bytes"": ANY, ""file_relative_path"": ""testdoc_google.docx""},
+            {""staging_file_url"": f""{TEST_LOCAL_DIRECTORY}/testdoc_google.docx"", ""bytes"": ANY, ""file_relative_path"": ""testdoc_google.docx""},
             False,
             id=""Read testdoc_google"",
         ),
@@ -749,12 +919,13 @@ def mock_next_chunk():
                 mime_type=""application/vnd.openxmlformats-officedocument.presentationml.presentation"",
                 id=""testdoc_presentation"",
                 original_mime_type=""application/vnd.google-apps.presentation"",
+                view_link=f""https://docs.google.com/presentation/d/testdoc_presentation/edit?usp=drivesdk"",
             ),
             b""test"",
             True,
             ""application/vnd.openxmlformats-officedocument.presentationml.presentation"",
             {
-                ""file_url"": ""/tmp/airbyte-file-transfer/testdoc_presentation.pptx"",
+                ""staging_file_url"": f""{TEST_LOCAL_DIRECTORY}/testdoc_presentation.pptx"",
                 ""bytes"": ANY,
                 ""file_relative_path"": ""testdoc_presentation.pptx"",
             },
@@ -766,7 +937,7 @@ def mock_next_chunk():
 @patch(""source_google_drive.stream_reader.MediaIoBaseDownload"")
 @patch(""source_google_drive.stream_reader.service_account"")
 @patch(""source_google_drive.stream_reader.build"")
-def test_download_file(
+def test_upload_file(
     mock_build_service,
     mock_service_account,
     mock_basedownload,
@@ -813,14 +984,90 @@ def mock_next_chunk(num_retries):
 
     if expect_raise:
         with pytest.raises(ValueError):
-            create_reader().get_file(file, local_directory=""tmp/airbyte-transfer"", logger=MagicMock())
+            create_reader().upload(file, local_directory=""tmp/airbyte-transfer"", logger=MagicMock())
     else:
-        file_paths = create_reader().get_file(file, local_directory=TEST_LOCAL_DIRECTORY, logger=MagicMock())
-        assert expected_paths[""file_url""] in file_paths[""file_url""]
-        assert expected_paths[""file_relative_path""] == file_paths[""file_relative_path""]
+        file_record_data, file_reference = create_reader().upload(file, local_directory=TEST_LOCAL_DIRECTORY, logger=MagicMock())
+        assert expected_paths[""staging_file_url""] in file_reference.staging_file_url
+        assert expected_paths[""file_relative_path""] == file_reference.source_file_relative_path
+        assert file.mime_type == file_record_data.mime_type
+
+        assert path.basename(expected_paths[""staging_file_url""]) == file_record_data.filename
+        assert path.dirname(expected_paths[""staging_file_url""].replace(f""{TEST_LOCAL_DIRECTORY}/"", """")) == file_record_data.folder
 
         assert mock_downloader.next_chunk.call_count == 2
         if expect_export:
             files_service.export_media.assert_has_calls([call(fileId=file.id, mimeType=expected_mime_type)])
+            assert expected_mime_type == file_record_data.mime_type
         else:
             files_service.get_media.assert_has_calls([call(fileId=file.id)])
+            assert file.mime_type == file_record_data.mime_type
+
+
+@pytest.mark.parametrize(
+    ""file, expected_source_uri"",
+    [
+        pytest.param(
+            GoogleDriveRemoteFile(
+                uri=""test.csv"",
+                last_modified=datetime.datetime(2023, 10, 16, 6, 16, 6),
+                mime_type=""text/csv"",
+                id=""123"",
+                original_mime_type=""text/csv"",
+                view_link=""https://docs.google.com/file/d/123/view?usp=drivesdk"",
+            ),
+            ""https://docs.google.com/file/d/123/view?usp=drivesdk"",
+            id=""My Drive file"",
+        ),
+        pytest.param(
+            GoogleDriveRemoteFile(
+                uri=""shared_drive_test.csv"",
+                last_modified=datetime.datetime(2023, 10, 16, 6, 16, 6),
+                mime_type=""text/csv"",
+                id=""456"",
+                original_mime_type=""text/csv"",
+                drive_id=""789"",
+                view_link=""https://docs.google.com/file/d/456/view?usp=drivesdk"",
+            ),
+            ""https://drive.google.com/open?id=456&driveId=789"",
+            id=""Shared Drive file"",
+        ),
+    ],
+)
+@patch(""source_google_drive.stream_reader.MediaIoBaseDownload"")
+@patch(""source_google_drive.stream_reader.service_account"")
+@patch(""source_google_drive.stream_reader.build"")
+def test_source_uri_format(
+    mock_build_service, mock_service_account, mock_basedownload, file: GoogleDriveRemoteFile, expected_source_uri: str
+):
+    mock_request = MagicMock()
+    mock_downloader = MagicMock()
+
+    def mock_next_chunk(num_retries):
+        handle = mock_basedownload.call_args[0][0]
+        total_size = 1024
+        mock_progress = MagicMock()
+        mock_progress.total_size = total_size
+        mock_progress.resumable_progress = handle.tell()
+
+        if handle.tell() > 0:
+            return (mock_progress, True)
+        else:
+            handle.write(b""test"")
+            return (mock_progress, False)
+
+    mock_downloader.next_chunk.side_effect = mock_next_chunk
+    mock_basedownload.return_value = mock_downloader
+
+    files_service = MagicMock()
+    mock_get = MagicMock()
+    mock_get.execute.return_value = {""size"": 1024}
+    files_service.get.return_value = mock_get
+
+    files_service.get_media.return_value = mock_request
+
+    drive_service = MagicMock()
+    drive_service.files.return_value = files_service
+    mock_build_service.return_value = drive_service
+
+    file_record_data, _ = create_reader().upload(file, local_directory=TEST_LOCAL_DIRECTORY, logger=MagicMock())
+    assert file_record_data.source_uri == expected_source_uri