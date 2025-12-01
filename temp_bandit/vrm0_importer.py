@@ -1043,9 +1043,10 @@ def load_vrm0_secondary_animation(
                 obj.parent_bone = bone_name
                 fixed_offset = [
                     offset[axis] * inv for axis, inv in zip([0, 2, 1], [-1, -1, 1])
-                ]  # TODO: Y軸反転はUniVRMのシリアライズに合わせてる
+                ]  # TODO: Y-axis inversion is matched to UniVRM serialization
 
-                # boneのtail側にparentされるので、根元からのpositionに動かしなおす
+                # Since it's parented to the tail side of the bone, move it to the
+                # position from the root
                 obj.matrix_world = Matrix.Translation(
                     [
                         armature.matrix_world.to_translation()[i]
@@ -1215,15 +1216,17 @@ def find_vrm_bone_node_indices(self) -> list[int]:
 
 
 def setup_bones(context: Context, armature: Object) -> None:
-    """"""Human Boneの方向と長さを設定する.
+    """"""Set the direction and length of Human Bones.
 
-    VRM0はボーンの方向と長さを持たないため、現在はインポート時にFORTUNEによる方向と長さ決めを行っている。
-    ただ、FORTUNEは人体の構造を考慮しないため、不自然なボーンになることがある。そのため、人体の構造を考慮した
-    ヒューリスティックな方式で方向と長さを決める。
+    VRM0 does not have bone direction and length, so currently FORTUNE's
+    direction and length determination is performed at import time. However,
+    since FORTUNE does not consider human body structure, it can result in
+    unnatural bones. Therefore, we determine direction and length using a
+    heuristic method that considers human body structure.
 
-    いつかやりたいこと:
-        Headの角度を、親の角度から30度以内に制限
-        ToesやFootが接地していない場合は仰角をつける。
+    Things to do someday:
+        Limit the Head angle to within 30 degrees from the parent angle.
+        Add elevation angle when Toes or Foot are not touching the ground.
     """"""
     armature_data = armature.data
     if not isinstance(armature_data, Armature):
@@ -1276,13 +1279,13 @@ def setup_bones(context: Context, armature: Object) -> None:
             bone_name,
             human_bone_name,
         ) in bone_name_to_human_bone_name.items():
-            # 現在のアルゴリズムでは
+            # The current algorithm cannot handle
             #
             #   head ---- node ---- leftEye
             #                   \
             #                    -- rightEye
             #
-            # を上手く扱えないので、leftEyeとrightEyeは処理しない
+            # well, so we don't process leftEye and rightEye
             if human_bone_name in [HumanBoneName.RIGHT_EYE, HumanBoneName.LEFT_EYE]:
                 continue
 
@@ -1355,9 +1358,11 @@ def setup_bones(context: Context, armature: Object) -> None:
                 continue
             human_bone_name_to_human_bone[n] = human_bone
 
-        # 目と頭のボーン以外のVRM Humanoidの先端のボーンに子が複数存在する場合
-        # 親と同じ方向に向ける。これでデフォルトよりも自然な方向になる。
-        # VRM制作者による方向指定かもしれないので、子が一つの場合は何もしない。
+        # When VRM Humanoid terminal bones other than eye and head bones have
+        # multiple children, point them in the same direction as the parent.
+        # This results in a more natural direction than the default.
+        # Since it might be a direction specification by the VRM creator,
+        # do nothing when there is only one child.
         for tip_bone_name in [
             HumanBoneName.JAW,
             HumanBoneName.LEFT_THUMB_DISTAL,
@@ -1376,14 +1381,15 @@ def setup_bones(context: Context, armature: Object) -> None:
             bone = None
             searching_tip_bone_name: Optional[HumanBoneName] = tip_bone_name
             while searching_tip_bone_name:
-                # 該当するボーンがあったらbreak
+                # Break if there is a corresponding bone
                 human_bone = human_bone_name_to_human_bone.get(searching_tip_bone_name)
                 if human_bone:
                     bone = armature_data.edit_bones.get(human_bone.node.bone_name)
                     if bone:
                         break
 
-                # 該当するボーンが無く、必須ボーンだった場合はデータのエラーのため中断
+                # If there is no corresponding bone and it was a required bone,
+                # abort due to data error
                 specification = HumanBoneSpecifications.get(searching_tip_bone_name)
                 if specification.requirement:
                     break
@@ -1394,7 +1400,8 @@ def setup_bones(context: Context, armature: Object) -> None:
                     )
                     break
 
-                # 親の子孫に割り当て済みのボーンがある場合は何もしない
+                # Do nothing if there are already assigned bones in the parent's
+                # descendants
                 assigned_parent_descendant_found = False
                 for parent_descendant in parent_specification.descendants():
                     parent_descendant_human_bone = human_bone_name_to_human_bone.get(
@@ -1424,9 +1431,10 @@ def setup_bones(context: Context, armature: Object) -> None:
             bone.roll = parent_bone.roll
             bone.tail = bone.head + parent_bone.vector / 2
 
-        # 目のボーンに子が無いか複数存在する場合、正面に向ける。
-        # これでデフォルトよりも自然な方向になる。
-        # VRM制作者による方向指定かもしれないので、子が一つの場合は何もしない。
+        # When eye bones have no children or multiple children, point them forward.
+        # This results in a more natural direction than the default.
+        # Since it might be a direction specification by the VRM creator,
+        # do nothing when there is only one child.
         for eye_human_bone in [
             human_bone_name_to_human_bone.get(HumanBoneName.LEFT_EYE),
             human_bone_name_to_human_bone.get(HumanBoneName.RIGHT_EYE),
@@ -1452,9 +1460,10 @@ def setup_bones(context: Context, armature: Object) -> None:
                 continue
             bone.tail = (Matrix.Translation(world_tail) @ world_inv).to_translation()
 
-        # 頭のボーンに子が無いか複数存在する場合、上に向ける。
-        # これでデフォルトよりも自然な方向になる。
-        # VRM制作者による方向指定かもしれないので、子が一つの場合は何もしない。
+        # When head bones have no children or multiple children, point them upward.
+        # This results in a more natural direction than the default.
+        # Since it might be a direction specification by the VRM creator,
+        # do nothing when there is only one child.
         for head_human_bone in [human_bone_name_to_human_bone.get(HumanBoneName.HEAD)]:
             if not head_human_bone or not head_human_bone.node.bone_name:
                 continue