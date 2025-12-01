@@ -52,10 +52,8 @@ def _merge_set_ui_element_requests(
         merged: dict[UIElementId, Any] = {}
         for request in requests:
             for ui_id, value in request.ids_and_values:
-                merged[UIElementId(ui_id)] = value
+                merged[ui_id] = value
         last_request = requests[-1]
-        # merged.keys() are already UIElementId since merged is dict[UIElementId, Any]
-        # Keys are already UIElementId type since merged is dict[UIElementId, Any]
         return SetUIElementValueRequest(
             object_ids=list(merged.keys()),
             values=list(merged.values()),