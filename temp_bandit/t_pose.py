@@ -240,8 +240,8 @@ def execute(self, context: Context, armature: Object) -> None:
 def reset_root_to_human_bone_translation(
     pose: Pose, ext: VrmAddonArmatureExtensionPropertyGroup
 ) -> None:
-    # ルートボーンからいずれかのHumanボーンまでの位置をリセット
-    # 全てのボーンをリセットしない理由は特に無くて勘
+    # Reset positions from root bone to any Human bone
+    # No particular reason for not resetting all bones, just intuition
     bones: list[PoseBone] = [bone for bone in pose.bones if not bone.parent]
     while bones:
         bone = bones.pop()
@@ -560,8 +560,8 @@ def load(
             pose_bone_pose = bone_name_to_pose_bone_pose.get(bone.name)
             if pose_bone_pose:
                 bone.matrix_basis = pose_bone_pose.matrix_basis.copy()
-                # bone.matrixを直接復元したほうが効率的に思えるが、それをやると
-                # コンストレイントがついている場合に不具合が発生することがある
+                # Directly restoring bone.matrix seems more efficient, but doing so
+                # can cause problems when constraints are attached
                 # https://github.com/saturday06/VRM-Addon-for-Blender/issues/671
                 bone.rotation_mode = pose_bone_pose.rotation_mode
                 bone.rotation_axis_angle = list(pose_bone_pose.rotation_axis_angle)
@@ -661,7 +661,8 @@ def setup_humanoid_t_pose(
         ext = get_armature_extension(armature_data)
         saved_vrm1_look_at_preview = ext.vrm1.look_at.enable_preview
         if ext.is_vrm1() and ext.vrm1.look_at.enable_preview:
-            # TODO: エクスポート時にここに到達する場合は事前に警告をすると親切
+            # TODO: It would be helpful to warn in advance if this is
+            # reached during export
             ext.vrm1.look_at.enable_preview = False
             if ext.vrm1.look_at.type == ext.vrm1.look_at.TYPE_BONE.identifier:
                 human_bones = ext.vrm1.humanoid.human_bones
@@ -690,7 +691,8 @@ def setup_humanoid_t_pose(
                     action, evaluation_time=pose_marker_frame
                 )
             else:
-                # TODO: エクスポート時にここに到達する場合は事前に警告をすると親切
+                # TODO: It would be helpful to warn in advance if this is
+                # reached during export
                 ops.vrm.make_estimated_humanoid_t_pose(
                     armature_object_name=armature.name
                 )
@@ -699,10 +701,9 @@ def setup_humanoid_t_pose(
 
     try:
         yield
-        # yield後にbpyのネイティブオブジェクトは削除されたりフレームが進んで
-        # 無効になることがある。その状態でアクセスするとクラッシュするため、
-        # yield後はその可能性のあるネイティブオブジェクトにアクセスしないように
-        # 注意する
+        # After yield, bpy native objects may be deleted or frames may advance
+        # making them invalid. Accessing them in this state can cause crashes,
+        # so be careful not to access potentially invalid native objects after yield
     finally:
         leave_setup_humanoid_t_pose(
             context,