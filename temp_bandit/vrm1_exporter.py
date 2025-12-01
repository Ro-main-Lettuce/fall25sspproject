@@ -2543,7 +2543,6 @@ def gltf_export_armature_object_remove(
                     if not bone.use_deform:
                         return False
 
-        # Armatureモディファイアがついていて、ウエイトがついていない頂点があったらFalse
         # https://github.com/KhronosGroup/glTF-Blender-IO/issues/2436
         armature_data_name_to_deform_bone_names: dict[str, set[str]] = {}
         for mesh_object_name in mesh_object_names:
@@ -2676,16 +2675,16 @@ def remove_exported_armature_object_before_4_2(
         node_dicts: list[Json],
         armature_node_index: int,
     ) -> None:
-        """"""Blender 4.2未満でシーンのアーマチュアオブジェクトが削除可能なら削除.
+        """"""Remove scene armature object if deletable in Blender versions before 4.2.
 
-        これはBlenderで再インポートした際に、Armatureのオブジェクトがボーン扱いされるのを
-        防ぐため。TODO: 本当はskin.skeletonなどを使って賢く処理するべき
+        This prevents Armature objects from being treated as bones when re-importing
+        in Blender. TODO: Should use skin.skeleton etc. for smarter processing
 
-        メインアーマチュアにトランスフォームが入っている場合、現在の方式では
-        Blender 4.2.1やUniVRM 0.126.0などでうまく処理できないためやらない
+        When the main armature has transforms, the current approach doesn't work well
+        with Blender 4.2.1 or UniVRM 0.126.0, so we don't do it
 
-        Skin Jointが登録されているルートボーンが複数ある場合は、skin.jointsは共通の
-        ルートボーンが必要な制約があるため、削除しない。
+        When there are multiple root bones registered as Skin Joints, skin.joints
+        requires a common root bone constraint, so we don't delete them.
         """"""
         if bpy.app.version >= (4, 2):
             return
@@ -2743,7 +2742,6 @@ def remove_exported_armature_object_before_4_2(
             if not isinstance(scene_node_indices, list):
                 continue
 
-            # シーンに属するノードのうち、そのアーマチュアの祖先ノードを削除
             for scene_node_index in list(scene_node_indices):
                 if not isinstance(scene_node_index, int):
                     continue
@@ -2775,7 +2773,6 @@ def remove_exported_armature_object_before_4_2(
                 scene_node_indices.append(armature_child_index)
                 if armature_replaced:
                     continue
-                # メインアーマチュアまでのワールド行列をその子供に適用
                 child_node_dict = node_dicts[armature_child_index]
                 if not isinstance(child_node_dict, dict):
                     continue