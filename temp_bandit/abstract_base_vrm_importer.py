@@ -131,10 +131,6 @@ def import_vrm(self) -> None:
                     self.context.view_layer.update()
                     progress.update(0.96)
 
-                    # テクスチャの展開を行う。その際に.blendファイルの保存が発生して
-                    # 保存時のコールバックが走ることがあるため、中途半端にインポート
-                    # されたVRMのデータに対してそのコールバックが適用されないように
-                    # 注意する
                     if self.preferences.extract_textures_into_folder:
                         self.extract_textures(repack=False)
                     elif bpy.app.version < (3, 1):
@@ -198,8 +194,6 @@ def save_bone_child_object_transforms(
             context.view_layer.update()
 
     def use_fake_user_for_thumbnail(self) -> None:
-        # サムネイルはVRMの仕様ではimageのインデックスとあるが、UniVRMの実装ではtexture
-        # のインデックスになっている
         # https://github.com/vrm-c/UniVRM/blob/v0.67.0/Assets/VRM/Runtime/IO/VRMImporterself.context.cs#L308
         meta_dict = self.parse_result.vrm0_extension_dict.get(""meta"")
         if not isinstance(meta_dict, dict):