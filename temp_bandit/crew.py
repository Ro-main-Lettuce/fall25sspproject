@@ -1220,6 +1220,10 @@ def copy(self):
             copied_data[""long_term_memory""] = self.long_term_memory.model_copy(deep=True)
         if self.entity_memory:
             copied_data[""entity_memory""] = self.entity_memory.model_copy(deep=True)
+        if self.external_memory:
+            copied_data[""external_memory""] = self.external_memory.model_copy(deep=True)
+        if self.user_memory:
+            copied_data[""user_memory""] = self.user_memory.model_copy(deep=True)
 
 
         copied_data.pop(""agents"", None)