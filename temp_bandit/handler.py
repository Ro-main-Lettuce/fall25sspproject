@@ -165,14 +165,15 @@ def calculate_collision(
 def update_pose_bone_rotations(context: Context, delta_time: float) -> None:
     pose_bone_and_rotations: list[tuple[PoseBone, Quaternion]] = []
 
-    for obj in context.blend_data.objects:
+    obj_list = [obj for obj in context.blend_data.objects if obj.type == ""ARMATURE""]
+
+    for obj in obj_list:
         calculate_object_pose_bone_rotations(delta_time, obj, pose_bone_and_rotations)
 
     for pose_bone, pose_bone_rotation in pose_bone_and_rotations:
         # pose_boneへの回転の代入は負荷が高いのでできるだけ実行しない
-        angle_diff = pose_bone_rotation.rotation_difference(
-            get_rotation_as_quaternion(pose_bone)
-        ).angle
+        current_rotation = get_rotation_as_quaternion(pose_bone)
+        angle_diff = pose_bone_rotation.rotation_difference(current_rotation).angle
         if abs(angle_diff) < float_info.epsilon:
             continue
         set_rotation_without_mode_change(pose_bone, pose_bone_rotation)
@@ -183,8 +184,6 @@ def calculate_object_pose_bone_rotations(
     obj: Object,
     pose_bone_and_rotations: list[tuple[PoseBone, Quaternion]],
 ) -> None:
-    if obj.type != ""ARMATURE"":
-        return
     armature_data = obj.data
     if not isinstance(armature_data, Armature):
         return
@@ -195,6 +194,9 @@ def calculate_object_pose_bone_rotations(
     if not spring_bone1.enable_animation:
         return
 
+    obj_matrix_world = obj.matrix_world
+    pose_bones_cache: dict[str, PoseBone] = {}
+
     collider_uuid_to_world_collider: dict[
         str,
         Union[
@@ -206,10 +208,14 @@ def calculate_object_pose_bone_rotations(
         ],
     ] = {}
     for collider in spring_bone1.colliders:
-        pose_bone = obj.pose.bones.get(collider.node.bone_name)
-        if not pose_bone:
-            continue
-        pose_bone_world_matrix = obj.matrix_world @ pose_bone.matrix
+        bone_name = collider.node.bone_name
+        pose_bone = pose_bones_cache.get(bone_name)
+        if pose_bone is None:
+            pose_bone = obj.pose.bones.get(bone_name)
+            if not pose_bone:
+                continue
+            pose_bones_cache[bone_name] = pose_bone
+        pose_bone_world_matrix = obj_matrix_world @ pose_bone.matrix
 
         extended_collider = collider.extensions.vrmc_spring_bone_extended_collider
         world_collider: Union[
@@ -353,11 +359,20 @@ def calculate_object_pose_bone_rotations(
         if not joints:
             continue
         first_joint = joints[0]
-        first_pose_bone = obj.pose.bones.get(first_joint.node.bone_name)
-        if not first_pose_bone:
-            continue
+        first_bone_name = first_joint.node.bone_name
+        first_pose_bone = pose_bones_cache.get(first_bone_name)
+        if first_pose_bone is None:
+            first_pose_bone = obj.pose.bones.get(first_bone_name)
+            if not first_pose_bone:
+                continue
+            pose_bones_cache[first_bone_name] = first_pose_bone
 
-        center_pose_bone = obj.pose.bones.get(spring.center.bone_name)
+        center_bone_name = spring.center.bone_name
+        center_pose_bone = pose_bones_cache.get(center_bone_name)
+        if center_pose_bone is None:
+            center_pose_bone = obj.pose.bones.get(center_bone_name)
+            if center_pose_bone:
+                pose_bones_cache[center_bone_name] = center_pose_bone
 
         # https://github.com/vrm-c/vrm-specification/blob/7279e169ac0dcf37e7d81b2adcad9107101d7e25/specification/VRMC_springBone-1.0/README.md#center-space
         center_pose_bone_is_ancestor_of_first_pose_bone = False
@@ -371,9 +386,8 @@ def calculate_object_pose_bone_rotations(
             center_pose_bone = None
 
         if center_pose_bone:
-            current_center_world_translation = (
-                obj.matrix_world @ center_pose_bone.matrix
-            ).to_translation()
+            center_world_matrix = obj_matrix_world @ center_pose_bone.matrix
+            current_center_world_translation = center_world_matrix.to_translation()
             previous_center_world_translation = Vector(
                 spring.animation_state.previous_center_world_translation
             )
@@ -435,6 +449,9 @@ def calculate_spring_pose_bone_rotations(
         ]
     ] = []
 
+    pose_bones_cache: dict[str, PoseBone] = {}
+    matrix_cache: dict[str, Matrix] = {}
+
     joints: list[
         tuple[
             SpringBone1JointPropertyGroup,
@@ -444,12 +461,21 @@ def calculate_spring_pose_bone_rotations(
     ] = []
     for joint in spring.joints:
         bone_name = joint.node.bone_name
-        pose_bone = obj.pose.bones.get(bone_name)
-        if not pose_bone:
-            continue
-        rest_object_matrix = pose_bone.bone.convert_local_to_pose(
-            Matrix(), pose_bone.bone.matrix_local
-        )
+        pose_bone = pose_bones_cache.get(bone_name)
+        if pose_bone is None:
+            pose_bone = obj.pose.bones.get(bone_name)
+            if not pose_bone:
+                continue
+            pose_bones_cache[bone_name] = pose_bone
+
+        matrix_key = f""rest_{bone_name}""
+        rest_object_matrix = matrix_cache.get(matrix_key)
+        if rest_object_matrix is None:
+            rest_object_matrix = pose_bone.bone.convert_local_to_pose(
+                Matrix(), pose_bone.bone.matrix_local
+            )
+            matrix_cache[matrix_key] = rest_object_matrix
+
         joints.append((joint, pose_bone, rest_object_matrix))
 
     for (head_joint, head_pose_bone, head_rest_object_matrix), (
@@ -547,6 +573,8 @@ def calculate_joint_pair_head_pose_bone_rotations(
     current_head_pose_bone_matrix = head_pose_bone.matrix
     current_tail_pose_bone_matrix = tail_pose_bone.matrix
 
+    obj_matrix_world = obj.matrix_world
+
     if next_head_pose_bone_before_rotation_matrix is None:
         if head_pose_bone.parent:
             current_head_parent_matrix = head_pose_bone.parent.matrix
@@ -555,22 +583,29 @@ def calculate_joint_pair_head_pose_bone_rotations(
                     Matrix(), head_pose_bone.parent.bone.matrix_local
                 )
             )
+            current_head_parent_rest_object_matrix_inv = (
+                current_head_parent_rest_object_matrix.inverted_safe()
+            )
+            next_head_pose_bone_before_rotation_matrix = current_head_parent_matrix @ (
+                current_head_parent_rest_object_matrix_inv
+                @ current_head_rest_object_matrix
+            )
         else:
             current_head_parent_matrix = Matrix()
-            current_head_parent_rest_object_matrix = Matrix()
-        next_head_pose_bone_before_rotation_matrix = current_head_parent_matrix @ (
-            current_head_parent_rest_object_matrix.inverted_safe()
-            @ current_head_rest_object_matrix
-        )
+            next_head_pose_bone_before_rotation_matrix = (
+                current_head_parent_matrix @ current_head_rest_object_matrix
+            )
 
-    next_head_world_translation = (
-        obj.matrix_world @ next_head_pose_bone_before_rotation_matrix.to_translation()
+    # Calculate matrix multiplication once and extract translation
+    next_head_matrix_world = (
+        obj_matrix_world @ next_head_pose_bone_before_rotation_matrix
     )
+    next_head_world_translation = next_head_matrix_world.to_translation().copy()
 
     if not tail_joint.animation_state.initialized_as_tail:
-        initial_tail_world_translation = (
-            obj.matrix_world @ current_tail_pose_bone_matrix
-        ).to_translation()
+        # Calculate matrix multiplication once and extract translation
+        tail_matrix_world = obj_matrix_world @ current_tail_pose_bone_matrix
+        initial_tail_world_translation = tail_matrix_world.to_translation()
         tail_joint.animation_state.initialized_as_tail = True
         tail_joint.animation_state.previous_world_translation = list(
             initial_tail_world_translation
@@ -608,9 +643,13 @@ def calculate_joint_pair_head_pose_bone_rotations(
         current_tail_world_translation + inertia + stiffness + external
     )
 
+    # Calculate matrix multiplications once and extract translations
+    head_world_matrix = obj_matrix_world @ current_head_pose_bone_matrix
+    tail_world_matrix = obj_matrix_world @ current_tail_pose_bone_matrix
+    head_world_translation = head_world_matrix.to_translation()
+    tail_world_translation = tail_world_matrix.to_translation()
     head_to_tail_world_distance = (
-        obj.matrix_world @ current_head_pose_bone_matrix.to_translation()
-        - (obj.matrix_world @ current_tail_pose_bone_matrix.to_translation())
+        head_world_translation - tail_world_translation
     ).length
 
     # 次のTailに距離の制約を適用
@@ -636,8 +675,9 @@ def calculate_joint_pair_head_pose_bone_rotations(
             * head_to_tail_world_distance
         )
 
+    obj_matrix_world_inv = obj_matrix_world.inverted_safe()
     next_tail_object_local_translation = (
-        obj.matrix_world.inverted_safe() @ next_tail_world_translation
+        obj_matrix_world_inv @ next_tail_world_translation
     )
     next_head_rotation_end_target_local_translation = (
         next_head_pose_bone_before_rotation_matrix.inverted_safe()