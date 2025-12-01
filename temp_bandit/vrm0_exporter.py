@@ -145,7 +145,7 @@ def create_index_search_key(
             texcoord: Optional[tuple[float, float]],
         ) -> IndexSearchKey:
             return (
-                # TODO: 旧エクスポーターと互換性のある形式
+                # TODO: Format compatible with old exporter
                 blender_vertex_index,
                 normal,
                 texcoord,
@@ -639,8 +639,8 @@ def write_extensions_vrm_secondary_animation(
                 ""stiffiness"": bone_group.stiffiness,
                 ""gravityPower"": bone_group.gravity_power,
                 ""gravityDir"": {
-                    # TODO: firstPerson.firstPersonBoneOffsetとBoneGroup.gravityDirの
-                    # 軸変換はオリジナルになっている。これについてコメントを記載する。
+                    # TODO: firstPerson.firstPersonBoneOffset and BoneGroup.gravityDir
+                    # axis conversion is original. Need to document this.
                     ""x"": bone_group.gravity_dir[0],
                     ""y"": bone_group.gravity_dir[2],
                     ""z"": bone_group.gravity_dir[1],
@@ -757,8 +757,8 @@ def write_extensions_vrm_first_person(
                 first_person_dict[""firstPersonBone""] = first_person_bone_index
 
         first_person_dict[""firstPersonBoneOffset""] = {
-            # TODO: firstPerson.firstPersonBoneOffsetとBoneGroup.gravityDirの
-            # 軸変換はオリジナルになっている。これについてコメントを記載する。
+            # TODO: firstPerson.firstPersonBoneOffset and BoneGroup.gravityDir
+            # axis conversion is original. Need to document this.
             ""x"": first_person.first_person_bone_offset[0],
             ""y"": first_person.first_person_bone_offset[2],
             ""z"": first_person.first_person_bone_offset[1],
@@ -1557,7 +1557,7 @@ def write_legacy_mtoon_unversioned_material(
 
         float_properties[""_CullMode""] = 2 if material.use_backface_culling else 0
 
-        # 旧エクスポーターとの互換性のため、テクスチャ追加順を制御している
+        # Control texture addition order for compatibility with old exporter
 
         main_tex = self.create_mtoon0_texture_info_dict(
             self.context,
@@ -1582,7 +1582,7 @@ def write_legacy_mtoon_unversioned_material(
             texture_properties[""_MainTex""] = main_tex_texture_property
             vector_properties[""_MainTex""] = main_tex_vector_property
 
-        # TODO: 互換性のためのもの。たぶん正しい設定値がある気がする
+        # TODO: For compatibility. There might be correct configuration values
         default_texture_vector_property = [0, 0, 1, 1]
 
         shade_texture = self.create_mtoon0_texture_info_dict(
@@ -2311,9 +2311,10 @@ def write_armature(
             )
             scene_node_indices: list[int] = [humanoid_root_bone_index]
         else:
-            # ルートボーンか複数ある場合、それぞれをシーンに展開する
-            # これは旧エクスポーターの仕様そのままだが、本当に正しいかは自信がない
-            # 親となるボーンを作り、それにskinをつけるのが本当は良いかもしれない
+            # If there are multiple root bones, expand each to the scene
+            # This follows the old exporter specification, but I'm not
+            # confident it's correct
+            # It might be better to create a parent bone and attach skin to it
             scene_node_indices = []
             for bone in bones:
                 root_node_index = self.write_armature_bone_nodes(
@@ -2326,8 +2327,8 @@ def write_armature(
                 )
                 scene_node_indices.append(root_node_index)
 
-                # Humanoidに属しているボーンがあるかを調べ、
-                # それをhumanoid_root_bone_indexとして設定
+                # Check if there are bones belonging to Humanoid,
+                # and set them as humanoid_root_bone_index
                 humanoid = get_armature_extension(self.armature_data).vrm0.humanoid
                 traversing_bones = [bone]
                 while traversing_bones:
@@ -2381,8 +2382,8 @@ def write_armature(
             }
         )
 
-        # Hitogata 0.6.0.1はskinを共有するとエラーになるようなので
-        # メッシュに対してそれぞれ内容の同じskinを持たせる
+        # Hitogata 0.6.0.1 seems to error when sharing skin,
+        # so give each mesh its own skin with the same content
         skin_dict: dict[str, Json] = {
             ""joints"": make_json(skin_joint_node_indices),
             ""inverseBindMatrices"": accessor_index,
@@ -2448,8 +2449,8 @@ def get_or_write_cluster_empty_material(
         material_dicts: list[dict[str, Json]],
         extensions_vrm_material_property_dicts: list[Json],
     ) -> int:
-        # clusterではマテリアル無しのプリミティブが許可されないため、
-        # 空のマテリアルを付与する。
+        # Cluster does not allow primitives without materials,
+        # so assign empty material.
         missing_material_name = ""glTF_2_0_default_material""
         for i, material_dict in enumerate(material_dicts):
             if material_dict.get(""name"") == missing_material_name:
@@ -2494,10 +2495,11 @@ def collect_vertex(
             texcoord_u, texcoord_v = uv_layer.data[loop_index].uv
             texcoord = (texcoord_u, 1 - texcoord_v)
 
-        # 頂点のノーマルではなくloopのノーマルを使う。これで失うものはあると
-        # 思うが、glTF 2.0アドオンと同一にしておくのが無難だろうと判断。
+        # Use loop normals instead of vertex normals. This may lose something,
+        # but it's judged safer to keep it the same as the glTF 2.0 addon.
         # https://github.com/KhronosGroup/glTF-Blender-IO/pull/1127
-        # TODO: この実装は本来はループを回った3つの法線を平均にするべき
+        # TODO: This implementation should really average the three normals
+        # from the loop
         normal = main_mesh_data.loops[loop_index].normal
 
         already_added_vertex_index = (
@@ -2527,7 +2529,7 @@ def collect_vertex(
                     )
                     is not None
                 )
-                # ウエイトがゼロの場合ジョイントもゼロにする
+                # Set joint to zero when weight is zero
                 # https://github.com/KhronosGroup/glTF/tree/f33f90ad9439a228bf90cde8319d851a52a3f470/specification/2.0#skinned-mesh-attributes
                 and not ((weight := vertex_group_element.weight) < float_info.epsilon)
             ]
@@ -2579,7 +2581,8 @@ def collect_vertex(
                         break
 
                 if joint is None:
-                    # TODO: たぶんhipsよりはhipsから辿ったルートボーンの方が良い
+                    # TODO: Probably better to use root bone traced from hips
+                    # rather than hips itself
                     ext = get_armature_extension(self.armature_data)
                     for human_bone in ext.vrm0.humanoid.human_bones:
                         if human_bone.bone != ""hips"":
@@ -2689,14 +2692,23 @@ def write_mesh_node(
         node_index = len(node_dicts)
         node_dict: dict[str, Json] = {
             ""name"": obj.name,
-            ""rotation"": [0, 0, 0, 1],  # TODO: デフォルト値と同一のため削除予定
-            ""scale"": [1, 1, 1],  # TODO: デフォルト値と同一のため削除予定
+            ""rotation"": [
+                0,
+                0,
+                0,
+                1,
+            ],  # TODO: Planned for removal as it's identical to default value
+            ""scale"": [
+                1,
+                1,
+                1,
+            ],  # TODO: Planned for removal as it's identical to default value
         }
 
         parent_node_index = None
         parent_translation = None
         if have_skin:
-            # スキンがある場合はシーンのルートノードになる
+            # Becomes scene root node when there's skin
             pass
         else:
             if (
@@ -2708,7 +2720,8 @@ def write_mesh_node(
                 )
                 and parent in self.export_objects
             ):
-                # TODO: 互換性のためネストしたメッシュを復元しないが、将来的には復元する
+                # TODO: Don't restore nested meshes for compatibility, but will
+                # restore in the future
                 # parent_translation = parent.matrix_world.to_translation()
                 # parent_node_index = object_name_to_node_index.get(parent.name)
                 pass
@@ -2771,13 +2784,14 @@ def write_mesh_node(
             shape_key_name_to_mesh_data: Optional[dict[str, Mesh]] = None
             shape_key_name_to_mesh_data = {}
             if original_shape_keys:
-                # シェイプキーごとにモディファイアを適用したメッシュを作成する。
-                # これは、VRM 0.x用にglTF Nodeの回転やスケールを正規化するが、
-                # ポーズモードで回転やスケールをつけた場合、その正規化のウエイト
-                # 計算がシェイプキーに適用されないため、シェイプキーごとの変化量を
-                # 自前で計算しなおす必要があるため。
-                # 頂点のインデックスなどが変わる可能性があるためダメなパターンも
-                # あると思うので、改善の余地あり。
+                # Create mesh with modifiers applied for each shape key.
+                # This is because for VRM 0.x, glTF Node rotation and scale
+                # are normalized, but when rotation or scale is applied in
+                # pose mode, the weight calculation for that normalization is
+                # not applied to shape keys, so we need to recalculate the
+                # change amount for each shape key ourselves.
+                # There might be bad patterns where vertex indices change,
+                # so there's room for improvement.
                 for shape_key in original_shape_keys.key_blocks:
                     if original_shape_keys.reference_key.name == shape_key.name:
                         continue
@@ -2795,7 +2809,7 @@ def write_mesh_node(
         obj.hide_viewport = False
         obj.hide_select = False
 
-        # TODO: 古いアドオンとの互換性のために移動を実行しているが、不要な気がする
+        # TODO: Executing move for compatibility with old addon, but seems unnecessary
         mesh_data_transform = Matrix.Identity(4)
         if not have_skin:
             mesh_data_transform @= Matrix.Translation(
@@ -2932,9 +2946,9 @@ def write_mesh_node(
         while len(buffer0) % 4:
             buffer0.append(0)
 
-        # TODO: buffer書き込み用のクラスを独立
+        # TODO: Make buffer writing class independent
 
-        # indicesの書き込み
+        # Write indices
         for (
             primitive_material_index,
             vertex_indices,
@@ -2956,7 +2970,7 @@ def write_mesh_node(
                     ""byteOffset"": 0,
                     ""type"": ""SCALAR"",
                     ""componentType"": GL_UNSIGNED_INT,
-                    # TODO: 割り算はミスを誘うので避ける
+                    # TODO: Avoid division as it can lead to mistakes
                     ""count"": int(len(vertex_indices) / 4),
                 }
             )
@@ -2967,7 +2981,7 @@ def write_mesh_node(
                 }
             )
 
-        # attributesは共有する仕様にした
+        # Made attributes shared by design
         primitive_attribute_dict: dict[str, Json] = {}
         for primitive_dict in primitive_dicts:
             primitive_dict[""attributes""] = primitive_attribute_dict
@@ -3023,7 +3037,7 @@ def write_mesh_node(
                 ""type"": ""VEC3"",
                 ""componentType"": GL_FLOAT,
                 ""count"": vertex_attributes_and_targets.count,
-                # ""normalized"": True, # TODO: 要調査
+                # ""normalized"": True, # TODO: Needs investigation
             }
         )
         primitive_attribute_dict[""NORMAL""] = normal_accessor_index
@@ -3103,7 +3117,7 @@ def write_mesh_node(
             )
             primitive_attribute_dict[""WEIGHTS_0""] = weights_accessor_index
 
-        # targetsは共有する仕様にした
+        # Made targets shared by design
         primitive_targets = vertex_attributes_and_targets.targets
         if primitive_targets:
             while len(buffer0) % 4:
@@ -3174,7 +3188,8 @@ def write_mesh_node(
             for primitive_dict in primitive_dicts:
                 primitive_dict[""targets""] = make_json(primitive_target_dicts)
                 primitive_dict[""extras""] = {
-                    # targetNamesはglTFの仕様には含まれないが、多くの実装で使われている
+                    # targetNames is not included in glTF specification, but is used
+                    # in many implementations
                     # https://github.com/KhronosGroup/glTF/blob/0251c5c0cce8daec69bd54f29f891e3d0cdb52c8/specification/2.0/Specification.adoc?plain=1#L1500-L1504
                     ""targetNames"": [target.name for target in primitive_targets]
                 }
@@ -3187,7 +3202,7 @@ def write_mesh_node(
         )
         mesh_object_name_to_mesh_index[obj.name] = mesh_index
         if skin_dict and have_skin:
-            # TODO: メッシュごとに別々のskinを作る
+            # TODO: Create separate skin for each mesh
             node_dict[""skin""] = len(skin_dicts)
             skin_dicts.append(dict(skin_dict))
 
@@ -3233,7 +3248,7 @@ def write_mesh_nodes(
             if mesh_object.type in search.MESH_CONVERTIBLE_OBJECT_TYPES
         ]
 
-        # メッシュを親子関係に従ってソート
+        # Sort meshes according to parent-child relationships
         while True:
             swapped = False
             for mesh_object in list(mesh_convertible_objects):
@@ -3341,10 +3356,9 @@ def clear_shape_key_values(self) -> Iterator[Mapping[tuple[str, str], float]]:
         )
         try:
             yield mesh_name_and_shape_key_name_to_value
-            # yield後にbpyのネイティブオブジェクトは削除されたりフレームが進んで
-            # 無効になることがある。その状態でアクセスするとクラッシュするため、
-            # yield後はその可能性のあるネイティブオブジェクトにアクセスしないように
-            # 注意する
+            # After yield, bpy native objects may be deleted or frames may advance
+            # making them invalid. Accessing them in this state can cause crashes,
+            # so be careful not to access potentially invalid native objects after yield
         finally:
             self.leave_clear_shape_key_values(
                 self.context, mesh_name_and_shape_key_name_to_value
@@ -3424,7 +3438,7 @@ def get_legacy_shader_images(self, material: Material) -> Sequence[Image]:
 
             return [image]
 
-        return list(dict.fromkeys(images).keys())  # 重複削除
+        return list(dict.fromkeys(images).keys())  # Remove duplicates
 
     def create_gltf2_io_texture(
         self,
@@ -3470,7 +3484,7 @@ def create_gltf2_io_texture(
                 r""^BlenderVrmAddonImport[0-9]+Image[0-9]+_"", """", source_name
             )
 
-            # 旧エクスポーターとの互換性のため、重複した命名を避ける
+            # Avoid duplicate naming for compatibility with old exporter
             image_name = image_base_name
             for count in range(100000):
                 if count:
@@ -3682,7 +3696,8 @@ def create_shape_key_name_to_vertex_index_to_morph_normal_diffs(
         reference_key_name: str,
     ) -> Mapping[str, tuple[tuple[float, float, float], ...]]:
         # logger.error(""CREATE UNIQ:"")
-        # 法線の差分を強制的にゼロにする設定が有効な頂点インデックスを集める
+        # Collect vertex indices where normal difference is forced to zero
+        # setting is enabled
         exclusion_vertex_indices: set[int] = set()
         for polygon in mesh_data.polygons:
             if not (0 <= polygon.material_index < len(mesh_data.materials)):
@@ -3710,14 +3725,14 @@ def create_shape_key_name_to_vertex_index_to_morph_normal_diffs(
 
         # logger.error(""KEY DIFF:"")
 
-        # シェイプキーごとの法線の値を集める
+        # Collect normal values for each shape key
         shape_key_name_to_vertex_normal_vectors: dict[str, list[Vector]] = {}
         for shape_key_name, shape_key_mesh_data in [
             (reference_key_name, mesh_data),
             *shape_key_name_to_mesh_data.items(),
         ]:
             # logger.error(""  refkey=%s key=%s"", reference_key_name, shape_key_name)
-            # 頂点のノーマルではなくsplit(loop)のノーマルを使う
+            # Use split (loop) normals instead of vertex normals
             # https://github.com/KhronosGroup/glTF-Blender-IO/pull/1129
             vertex_normal_sum_vectors = [Vector([0.0, 0.0, 0.0])] * len(
                 mesh_data.vertices
@@ -3739,7 +3754,8 @@ def create_shape_key_name_to_vertex_index_to_morph_normal_diffs(
                         # logger.error(""      OUT OF RANGE"")
                         continue
                     vertex_normal_sum_vectors[vertex_index] = (
-                        # 普通は += 演算子を使うが、なぜか結果が変わるので使わない
+                        # Normally we would use the += operator, but for some
+                        # reason the result changes so we don't use it
                         vertex_normal_sum_vectors[vertex_index] + Vector(normal)
                     )
                     # logger.error(
@@ -3758,7 +3774,7 @@ def create_shape_key_name_to_vertex_index_to_morph_normal_diffs(
             reference_key_name
         ]
 
-        # シェイプキーごとに、リファレンスキーとの法線の差分を集める
+        # Collect normal differences from reference key for each shape key
         shape_key_name_to_vertex_index_to_morph_normal_diffs: dict[
             str, tuple[tuple[float, float, float], ...]
         ] = {}
@@ -3803,8 +3819,8 @@ def create_shape_key_name_to_vertex_index_to_morph_normal_diffs(
         return shape_key_name_to_vertex_index_to_morph_normal_diffs
 
     def have_skin(self, mesh: Object) -> bool:
-        # TODO: このメソッドは誤判定があるが互換性のためにそのままになっている。
-        # 将来的には正しい実装に置き換わる
+        # TODO: This method has false positives but is kept as-is for compatibility.
+        # In the future, this will be replaced with correct implementation
         while mesh:
             if any(
                 modifier.show_viewport and modifier.type == ""ARMATURE""