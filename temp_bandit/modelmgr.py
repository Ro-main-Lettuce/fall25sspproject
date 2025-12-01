@@ -174,9 +174,16 @@ async def remove_embedding_model(self, model_uuid: str):
                 self.embedding_models.remove(model)
                 return
 
-    def get_available_requesters_info(self) -> list[dict]:
+    def get_available_requesters_info(self, model_type: str) -> list[dict]:
         """"""获取所有可用的请求器""""""
-        return [component.to_plain_dict() for component in self.requester_components]
+        if model_type != '':
+            return [
+                component.to_plain_dict()
+                for component in self.requester_components
+                if model_type in component.spec['support_type']
+            ]
+        else:
+            return [component.to_plain_dict() for component in self.requester_components]
 
     def get_available_requester_info_by_name(self, name: str) -> dict | None:
         """"""通过名称获取请求器信息""""""