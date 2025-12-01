@@ -33,7 +33,7 @@ def test_csv_knowledge_source_updates(mock_add, mock_search, tmpdir):
         for row in initial_csv_content:
             f.write("","".join(row) + ""
"")
     
-    csv_source = CSVKnowledgeSource(file_paths=csv_path)
+    csv_source = CSVKnowledgeSource(file_paths=[csv_path])
     
     original_files_have_changed = csv_source.files_have_changed
     files_changed_called = [False]
@@ -65,7 +65,8 @@ def spy_files_have_changed():
     
     time.sleep(1)
     
-    with open(csv_path, ""w"") as f:
+    csv_path_str = str(csv_path)
+    with open(csv_path_str, ""w"") as f:
         for row in updated_csv_content:
             f.write("","".join(row) + ""
"")
     