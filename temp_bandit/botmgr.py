@@ -248,7 +248,9 @@ async def remove_bot(self, bot_uuid: str):
                 return
 
     def get_available_adapters_info(self) -> list[dict]:
-        return [component.to_plain_dict() for component in self.adapter_components]
+        return [
+            component.to_plain_dict() for component in self.adapter_components if component.metadata.name != 'webchat'
+        ]
 
     def get_available_adapter_info_by_name(self, name: str) -> dict | None:
         for component in self.adapter_components: