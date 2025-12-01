@@ -409,7 +409,7 @@ def create_look_at_animation(
     ]
     input_bytes = struct.pack(""<"" + ""f"" * len(input_floats), *input_floats)
     buffer0_bytearray.extend(input_bytes)
-    while len(buffer0_bytearray) % 32 != 0:  # TODO: 正しいアラインメントを調べる
+    while len(buffer0_bytearray) % 32 != 0:  # TODO: Find the correct alignment
         buffer0_bytearray.append(0)
     input_buffer_view_index = len(buffer_view_dicts)
     input_buffer_view_dict: dict[str, Json] = {
@@ -434,7 +434,7 @@ def create_look_at_animation(
         ""<"" + ""f"" * len(translation_floats), *translation_floats
     )
     buffer0_bytearray.extend(translation_bytes)
-    while len(buffer0_bytearray) % 32 != 0:  # TODO: 正しいアラインメントを調べる
+    while len(buffer0_bytearray) % 32 != 0:  # TODO: Find the correct alignment
         buffer0_bytearray.append(0)
     output_buffer_view_index = len(buffer_view_dicts)
     output_buffer_view_dict: dict[str, Json] = {
@@ -601,7 +601,7 @@ def create_expression_animation(
         ]
         input_bytes = struct.pack(""<"" + ""f"" * len(input_floats), *input_floats)
         buffer0_bytearray.extend(input_bytes)
-        while len(buffer0_bytearray) % 32 != 0:  # TODO: 正しいアラインメントを調べる
+        while len(buffer0_bytearray) % 32 != 0:  # TODO: Find the correct alignment
             buffer0_bytearray.append(0)
         input_buffer_view_index = len(buffer_view_dicts)
         input_buffer_view_dict: dict[str, Json] = {
@@ -621,7 +621,7 @@ def create_expression_animation(
             *expression_translation_floats,
         )
         buffer0_bytearray.extend(translation_bytes)
-        while len(buffer0_bytearray) % 32 != 0:  # TODO: 正しいアラインメントを調べる
+        while len(buffer0_bytearray) % 32 != 0:  # TODO: Find the correct alignment
             buffer0_bytearray.append(0)
         output_buffer_view_index = len(buffer_view_dicts)
         output_buffer_view_dict: dict[str, Json] = {
@@ -793,8 +793,8 @@ def create_node_animation(
         if base_quaternion is None:
             continue
         bone_name_to_quaternions[bone_name] = [
-            # ミュートされている項目とかあるとクオータニオンの値がノーマライズされて
-            # いないのでノーマライズしておく
+            # Muted items and other factors may cause quaternion values to be
+            # denormalized, so we normalize them
             base_quaternion @ quaternion_offset.normalized()
             for quaternion_offset in quaternion_offsets
         ]
@@ -818,7 +818,7 @@ def create_node_animation(
             for axis_angle_offset in axis_angle_offsets
         ]
 
-    # 回転のエクスポート
+    # Export rotation
     for bone_name, quaternions in bone_name_to_quaternions.items():
         human_bone_name = next(
             (
@@ -844,7 +844,7 @@ def create_node_animation(
         ]
         input_bytes = struct.pack(""<"" + ""f"" * len(input_floats), *input_floats)
         buffer0_bytearray.extend(input_bytes)
-        while len(buffer0_bytearray) % 32 != 0:  # TODO: 正しいアラインメントを調べる
+        while len(buffer0_bytearray) % 32 != 0:  # TODO: Find the correct alignment
             buffer0_bytearray.append(0)
         input_buffer_view_index = len(buffer_view_dicts)
         input_buffer_view_dict: dict[str, Json] = {
@@ -870,7 +870,7 @@ def create_node_animation(
             ""<"" + ""f"" * len(quaternion_floats), *quaternion_floats
         )
         buffer0_bytearray.extend(quaternion_bytes)
-        while len(buffer0_bytearray) % 32 != 0:  # TODO: 正しいアラインメントを調べる
+        while len(buffer0_bytearray) % 32 != 0:  # TODO: Find the correct alignment
             buffer0_bytearray.append(0)
         output_buffer_view_index = len(buffer_view_dicts)
         output_buffer_view_dict: dict[str, Json] = {
@@ -931,7 +931,7 @@ def create_node_animation(
             }
         )
 
-    # hipsの平行移動のエクスポート
+    # Export hips translation
     hips_bone_name = human_bones.hips.node.bone_name
 
     hips_bone = armature.pose.bones.get(hips_bone_name)
@@ -947,7 +947,7 @@ def create_node_animation(
     else:
         base_matrix = Matrix()
     hips_translations = [
-        # TODO: 回転と同じように、RESTポーズとTポーズの差分を取るべき
+        # TODO: Find the correct alignment
         base_matrix @ hips_bone.matrix @ hips_translation_offset
         for hips_translation_offset in hips_translation_offsets
     ]
@@ -961,7 +961,7 @@ def create_node_animation(
     ]
     input_bytes = struct.pack(""<"" + ""f"" * len(input_floats), *input_floats)
     buffer0_bytearray.extend(input_bytes)
-    while len(buffer0_bytearray) % 32 != 0:  # TODO: 正しいアラインメントを調べる
+    while len(buffer0_bytearray) % 32 != 0:  # TODO: Find the correct alignment
         buffer0_bytearray.append(0)
     input_buffer_view_index = len(buffer_view_dicts)
     input_buffer_view_dict = {
@@ -986,7 +986,7 @@ def create_node_animation(
         ""<"" + ""f"" * len(translation_floats), *translation_floats
     )
     buffer0_bytearray.extend(translation_bytes)
-    while len(buffer0_bytearray) % 32 != 0:  # TODO: 正しいアラインメントを調べる
+    while len(buffer0_bytearray) % 32 != 0:  # TODO: Find the correct alignment
         buffer0_bytearray.append(0)
     output_buffer_view_index = len(buffer_view_dicts)
     output_buffer_view_dict = {