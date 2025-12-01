@@ -672,6 +672,7 @@ def handle_genai_structured_outputs(
     new_kwargs.pop(""messages"", None)
     new_kwargs.pop(""generation_config"", None)
     new_kwargs.pop(""safety_settings"", None)
+    new_kwargs.pop(""context"", None)
 
     return response_model, new_kwargs
 
@@ -738,6 +739,7 @@ def handle_genai_tools(
     new_kwargs.pop(""messages"", None)
     new_kwargs.pop(""generation_config"", None)
     new_kwargs.pop(""safety_settings"", None)
+    new_kwargs.pop(""context"", None)
 
     return response_model, new_kwargs
 