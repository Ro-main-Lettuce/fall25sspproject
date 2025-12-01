@@ -72,12 +72,13 @@ def assign_texture_colorspace(image: Image, preferred_colorspace: str) -> None:
         colorspace_settings = image.colorspace_settings
         exceptions: list[Exception] = []
         for colorspace in colorspaces:
-            # colorspace_settings.nameに設定可能な値はBlenderのセットアップにより
-            # 変化する。例えばpypiのbpy 3.6.0はLinearかsRGBかしか選べない。
-            # それを検知するため 本来なら
+            # The values that can be set in colorspace_settings.name vary
+            # depending on the Blender setup. For example, bpy 3.6.0 from pypi
+            # can only choose Linear or sRGB.
+            # To detect this, we would ideally want to reference
             # colorspace_settings.bl_rna.properties.get(""name"").enum_items
-            # などを参照したいが、Blender 2.93などでクラッシュするため使えない。
-            # 仕方がないので例外を拾いつつ代入が成功するまで試行する。
+            # etc., but it cannot be used because it crashes in Blender 2.93 etc.
+            # So we catch exceptions and try until assignment succeeds.
             try:
                 colorspace_settings.name = colorspace
             except TypeError as e:
@@ -542,20 +543,21 @@ def setup_vrm1_humanoid_bones(self) -> None:
                     human_bone_name
                 )
 
-            # ボーンの子が複数ある場合
-            # そのボーン名からテールを向ける先の子ボーン名を拾えるdictを作る
+            # When a bone has multiple children
+            # Create a dict to pick the child bone name to point the tail to
+            # from that bone name
             bone_name_to_main_child_bone_name: dict[str, str] = {}
             for (
                 bone_name,
                 human_bone_name,
             ) in bone_name_to_human_bone_name.items():
-                # 現在のアルゴリズムでは
+                # The current algorithm cannot handle
                 #
                 #   head ---- node ---- leftEye
                 #                   \
                 #                    -- rightEye
                 #
-                # を上手く扱えないので、leftEyeとrightEyeは処理しない
+                # well, so we don't process leftEye and rightEye
                 if human_bone_name in [HumanBoneName.RIGHT_EYE, HumanBoneName.LEFT_EYE]:
                     continue
 
@@ -619,7 +621,7 @@ def setup_vrm1_humanoid_bones(self) -> None:
                     bone_name_to_main_child_bone_name[parent.name] = bone.name
                     bone = parent
 
-            # ヒューマンボーンとその先祖ボーンを得る
+            # Get human bones and their ancestor bones
             human_bone_tree_bone_names: set[str] = set()
             for bone_name in bone_name_to_human_bone_name:
                 bone = armature_data.edit_bones.get(bone_name)
@@ -700,9 +702,10 @@ def setup_vrm1_humanoid_bones(self) -> None:
                 if not found:
                     constraint_node_index_groups.append({node_index, source_index})
 
-            # 軸変換時コンストレイントがついている場合にヒューマンボーンと
-            # その先祖ボーンを優先したいので、それらを深さ優先で先に処理し、
-            # その後その他のボーンを深さ優先で処理する
+            # When constraints are attached during axis conversion, we want to
+            # prioritize human bones and their ancestor bones, so we process
+            # them first in depth-first order, then process other bones in
+            # depth-first order
             unsorted_bones = [
                 bone for bone in armature_data.edit_bones if not bone.parent
             ]
@@ -1501,7 +1504,7 @@ def load_spring_bone1_collider(
 
             collider_bpy_object = collider.bpy_object
             if collider_bpy_object:
-                # フォールバックのコライダーをロードする際に入った値を固定値で上書きする
+                # Override the fallback collider values with fixed values when loading
                 collider_bpy_object.empty_display_size = 0.125
 
         else:
@@ -1521,8 +1524,8 @@ def load_spring_bone1_colliders(
             collider_dicts = []
 
         for collider_dict in collider_dicts:
-            # ColliderGroupからColliderへの参照はindexでの参照のため、
-            # collider_dictの中身が不正でも空のデータは作成しておく
+            # Since the reference from ColliderGroup to Collider is by index,
+            # create empty data even if the contents of collider_dict are invalid
             if ops.vrm.add_spring_bone1_collider(
                 armature_object_name=armature.name
             ) != {""FINISHED""}:
@@ -1581,8 +1584,8 @@ def load_spring_bone1_collider_groups(
         for collider_group_index, collider_group_dict in enumerate(
             collider_group_dicts
         ):
-            # SpringからColliderGroupへの参照はindexでの参照のため、
-            # collider_group_dictの中身が不正でも空のデータは作成しておく
+            # Since the reference from Spring to ColliderGroup is by index,
+            # create empty data even if the contents of collider_group_dict are invalid
             if ops.vrm.add_spring_bone1_collider_group(
                 armature_object_name=armature_object_name
             ) != {""FINISHED""}:
@@ -1863,7 +1866,7 @@ def load_node_constraint1(
             else:
                 continue
 
-            # TODO: mypyが賢くなったら消す
+            # TODO: Remove this when mypy becomes smarter
             if not isinstance(  # pyright: ignore [reportUnnecessaryIsInstance]
                 constraint,
                 (CopyRotationConstraint, DampedTrackConstraint),