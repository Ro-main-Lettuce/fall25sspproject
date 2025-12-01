@@ -310,21 +310,21 @@ def get_bone_name(self) -> str:
             return """"
         if not self.armature_data_name:
             return """"
-        
+
         cache_key = (self.armature_data_name, self.bone_uuid)
         cached_bone_name = self.armature_data_name_and_bone_uuid_to_bone_name_cache.get(
             cache_key
         )
-        
+
         if cached_bone_name is not None:
             if cached_bone_name == """":
                 return """"
-                
+
             # armature_dataのチェックは実際に骨名が有効な場合のみ行う
             armature_data = context.blend_data.armatures.get(self.armature_data_name)
             if not armature_data:
                 return """"
-                
+
             if (
                 cached_bone := armature_data.bones.get(cached_bone_name)
             ) and get_bone_extension(cached_bone).uuid == self.bone_uuid: