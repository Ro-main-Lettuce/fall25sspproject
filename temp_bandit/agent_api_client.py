@@ -337,6 +337,8 @@ def get_template_path_from_id(template_id: Optional[str]) -> str:
         return ""./trpc_agent/template""
     elif template_id == ""nicegui_agent"":
         return ""./nicegui_agent/template""
+    elif template_id == ""laravel_agent"":
+        return ""./laravel_agent/template""
     elif template_id == ""template_diff"":
         return ""./template_diff/template""
     else: