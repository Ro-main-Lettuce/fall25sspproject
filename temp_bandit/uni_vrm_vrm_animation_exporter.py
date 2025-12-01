@@ -411,7 +411,7 @@ def create_look_at_animation(
     ]
     input_bytes = struct.pack(""<"" + ""f"" * len(input_floats), *input_floats)
     buffer0_bytearray.extend(input_bytes)
-    while len(buffer0_bytearray) % 32 != 0:  # TODO: 正しいアラインメントを調べる
+    while len(buffer0_bytearray) % 32 != 0:  # TODO: Find the correct alignment
         buffer0_bytearray.append(0)
     input_buffer_view_index = len(buffer_view_dicts)
     input_buffer_view_dict: dict[str, Json] = {
@@ -436,7 +436,7 @@ def create_look_at_animation(
         ""<"" + ""f"" * len(translation_floats), *translation_floats
     )
     buffer0_bytearray.extend(translation_bytes)
-    while len(buffer0_bytearray) % 32 != 0:  # TODO: 正しいアラインメントを調べる
+    while len(buffer0_bytearray) % 32 != 0:  # TODO: Find the correct alignment
         buffer0_bytearray.append(0)
     output_buffer_view_index = len(buffer_view_dicts)
     output_buffer_view_dict: dict[str, Json] = {
@@ -603,7 +603,7 @@ def create_expression_animation(
         ]
         input_bytes = struct.pack(""<"" + ""f"" * len(input_floats), *input_floats)
         buffer0_bytearray.extend(input_bytes)
-        while len(buffer0_bytearray) % 32 != 0:  # TODO: 正しいアラインメントを調べる
+        while len(buffer0_bytearray) % 32 != 0:  # TODO: Find the correct alignment
             buffer0_bytearray.append(0)
         input_buffer_view_index = len(buffer_view_dicts)
         input_buffer_view_dict: dict[str, Json] = {
@@ -623,7 +623,7 @@ def create_expression_animation(
             *expression_translation_floats,
         )
         buffer0_bytearray.extend(translation_bytes)
-        while len(buffer0_bytearray) % 32 != 0:  # TODO: 正しいアラインメントを調べる
+        while len(buffer0_bytearray) % 32 != 0:  # TODO: Find the correct alignment
             buffer0_bytearray.append(0)
         output_buffer_view_index = len(buffer_view_dicts)
         output_buffer_view_dict: dict[str, Json] = {
@@ -789,7 +789,7 @@ def create_node_animation(
             continue
         hips_translations.append(hips_pose_bone.matrix.to_translation())
 
-    # 回転のエクスポート
+    # Export rotation
     for bone_name, quaternions in bone_name_to_quaternions.items():
         if all(abs(quaternion.angle) == 0 for quaternion in quaternions):
             continue
@@ -817,7 +817,7 @@ def create_node_animation(
         ]
         input_bytes = struct.pack(""<"" + ""f"" * len(input_floats), *input_floats)
         buffer0_bytearray.extend(input_bytes)
-        while len(buffer0_bytearray) % 32 != 0:  # TODO: 正しいアラインメントを調べる
+        while len(buffer0_bytearray) % 32 != 0:  # TODO: Find the correct alignment
             buffer0_bytearray.append(0)
         input_buffer_view_index = len(buffer_view_dicts)
         input_buffer_view_dict: dict[str, Json] = {
@@ -843,7 +843,7 @@ def create_node_animation(
             ""<"" + ""f"" * len(quaternion_floats), *quaternion_floats
         )
         buffer0_bytearray.extend(quaternion_bytes)
-        while len(buffer0_bytearray) % 32 != 0:  # TODO: 正しいアラインメントを調べる
+        while len(buffer0_bytearray) % 32 != 0:  # TODO: Find the correct alignment
             buffer0_bytearray.append(0)
         output_buffer_view_index = len(buffer_view_dicts)
         output_buffer_view_dict: dict[str, Json] = {
@@ -904,7 +904,7 @@ def create_node_animation(
             }
         )
 
-    # hipsの平行移動のエクスポート
+    # Export hips translation
     hips_node_index = bone_name_to_node_index.get(hips_bone_name)
     if hips_node_index is None:
         logger.error(""Failed to find node index for hips bone %s"", hips_bone_name)
@@ -920,7 +920,7 @@ def create_node_animation(
     ]
     input_bytes = struct.pack(""<"" + ""f"" * len(input_floats), *input_floats)
     buffer0_bytearray.extend(input_bytes)
-    while len(buffer0_bytearray) % 32 != 0:  # TODO: 正しいアラインメントを調べる
+    while len(buffer0_bytearray) % 32 != 0:  # TODO: Find the correct alignment
         buffer0_bytearray.append(0)
     input_buffer_view_index = len(buffer_view_dicts)
     input_buffer_view_dict = {
@@ -945,7 +945,7 @@ def create_node_animation(
         ""<"" + ""f"" * len(translation_floats), *translation_floats
     )
     buffer0_bytearray.extend(translation_bytes)
-    while len(buffer0_bytearray) % 32 != 0:  # TODO: 正しいアラインメントを調べる
+    while len(buffer0_bytearray) % 32 != 0:  # TODO: Find the correct alignment
         buffer0_bytearray.append(0)
     output_buffer_view_index = len(buffer_view_dicts)
     output_buffer_view_dict = {