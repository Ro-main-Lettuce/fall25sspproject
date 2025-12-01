@@ -1,3 +1,4 @@
+import keyword
 import shutil
 import tempfile
 from pathlib import Path
@@ -169,8 +170,6 @@ def test_create_folder_structure_raises_error_for_invalid_names():
 
 
 def test_create_folder_structure_validates_names():
-    import keyword
-    
     with tempfile.TemporaryDirectory() as temp_dir:
         valid_cases = [
             (""hello/"", ""hello"", ""Hello""),
@@ -207,6 +206,12 @@ def test_create_crew_with_parent_folder_and_trailing_slash(mock_load_env, mock_w
     with tempfile.TemporaryDirectory() as work_dir:
         parent_path = Path(work_dir) / ""parent""
         parent_path.mkdir()
+        
+        create_crew(""child-crew/"", skip_provider=True, parent_folder=parent_path)
+        
+        crew_path = parent_path / ""child_crew""
+        assert crew_path.exists()
+        assert not (crew_path / ""src"").exists()
 
 
 def test_create_folder_structure_folder_name_validation():
@@ -239,10 +244,3 @@ def test_create_folder_structure_folder_name_validation():
             
             if folder_path.exists():
                 shutil.rmtree(folder_path)
-
-        
-        create_crew(""child-crew/"", skip_provider=True, parent_folder=parent_path)
-        
-        crew_path = parent_path / ""child_crew""
-        assert crew_path.exists()
-        assert not (crew_path / ""src"").exists()