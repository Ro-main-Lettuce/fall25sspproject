@@ -69,6 +69,7 @@ def test_transform_to_json_does_not_mutate_keys(valid_metadata_upload_files, val
         ""data.releases.rolloutConfiguration.advanceDelayMinutes"",
         ""data.releases.breakingChanges.2.0.0.deadlineAction"",
         ""data.ab_internal.isEnterprise"",
+        ""data.ab_internal.requireVersionIncrementsInPullRequests"",
     ]
 
     for file_path in all_valid_metadata_files: