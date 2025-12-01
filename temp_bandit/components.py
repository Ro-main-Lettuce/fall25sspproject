@@ -677,7 +677,11 @@ def next_page_token(
         if (last_page_size < self.page_size) or last_page_size == 0 or not response.json().get(""paging""):
             return None
 
-        return {""after"": last_page_token_value[""after""] + last_page_size}
+        last_id_of_previous_chunk = last_page_token_value.get(""id"")
+        if last_id_of_previous_chunk:
+            return {""after"": last_page_token_value[""after""] + last_page_size, self.primary_key: last_id_of_previous_chunk}
+        else:
+            return {""after"": last_page_token_value[""after""] + last_page_size}
 
     def get_page_size(self) -> Optional[int]:
         return self.page_size