@@ -71,19 +71,15 @@ def convert_url_path_to_github_path(url_path) -> str:
 
         path_no_slashes = string_replace_operation(url_path, r""^/+|/+$"", """")
         path_clean = string_replace_operation(path_no_slashes, r""/+"", ""/"")
-        
         path_without_docs = string_replace_operation(path_clean, ""^docs/"", """")
         
-        result_path = path_without_docs
-        url_to_filepath_map = _get_url_to_filepath_mapping()
-        for browser_url, file_path in url_to_filepath_map.items():
-            if browser_url != file_path.replace('.md', ''):
-                result_path = string_replace_operation(result_path, browser_url, file_path.replace('.md', ''))
+        path_converted = string_replace_operation(path_without_docs, ""-"", ""_"")
+        
+        final_path = path_converted
+        if not path_converted._js_expr.endswith("".md""):
+            final_path = path_converted + "".md""
         
-        final_path = result_path
-        if not result_path._js_expr.endswith("".md""):
-            final_path = result_path + "".md""
-        return final_path
+        return ""docs/"" + final_path
     else:
         path = str(url_path).strip(""/"")
         while ""//"" in path: