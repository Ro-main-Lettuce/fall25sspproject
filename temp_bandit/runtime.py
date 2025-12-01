@@ -1629,7 +1629,7 @@ async def set_ui_element_value(
                         child_context.app is not None
                         and await child_context.app.set_ui_element_value(
                             SetUIElementValueRequest(
-                                object_ids=[UIElementId(object_id)],
+                                object_ids=[object_id],
                                 values=[value],
                                 request=request.request,
                             )
@@ -1654,16 +1654,15 @@ async def set_ui_element_value(
                     ""Could not resolve UIElement with id%s"", object_id
                 )
                 continue
-            resolved_requests[UIElementId(resolved_id)] = resolved_value
+            resolved_requests[resolved_id] = resolved_value
         del request
 
         for object_id, value in resolved_requests.items():
             try:
-                ui_id = UIElementId(object_id)
-                component = ui_element_registry.get_object(ui_id)
+                component = ui_element_registry.get_object(object_id)
                 LOGGER.debug(
                     ""Setting value on UIElement with id %s, value %s"",
-                    ui_id,
+                    object_id,
                     value,
                 )
             except KeyError: