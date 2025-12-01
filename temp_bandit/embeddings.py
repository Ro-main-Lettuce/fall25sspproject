@@ -62,7 +62,12 @@ def handle_embeddings_attributes(
             response_dict = model_as_dict(return_value)
         elif isinstance(return_value, dict):
             response_dict = return_value
-
+        elif hasattr(return_value, ""model_dump""):
+            # Handle Pydantic models directly
+            response_dict = return_value.model_dump()
+        elif hasattr(return_value, ""__dict__""):
+            # Try to use model_as_dict even if it has __iter__
+            response_dict = model_as_dict(return_value)
         # Basic response attributes
         if ""model"" in response_dict:
             attributes[SpanAttributes.LLM_RESPONSE_MODEL] = response_dict[""model""]