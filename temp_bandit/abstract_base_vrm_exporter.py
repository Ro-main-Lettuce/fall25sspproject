@@ -161,10 +161,10 @@ def hide_mtoon1_outline_geometry_nodes(context: Context) -> Iterator[None]:
 
     @staticmethod
     def setup_mtoon_gltf_fallback_nodes(context: Context, *, is_vrm0: bool) -> None:
-        """"""MToonのノードの値を、glTFのフォールバック値に使われるノードに反映する.
+        """"""Reflect MToon node values to nodes used for glTF fallback values.
 
-        MToonのノードを直接編集した場合、glTFのフォールバック値は自動で設定されない。
-        そのためエクスポート時に明示的に値を設定する。
+        When editing MToon nodes directly, glTF fallback values aren't set auto.
+        Therefore, values are explicitly set during export.
         """"""
         for material in context.blend_data.materials:
             mtoon1 = get_material_extension(material).mtoon1
@@ -216,8 +216,6 @@ def force_apply_modifiers(
     if not persistent:
         return evaluated_temporary_mesh.copy()
 
-    # ドキュメントにはBlendDataMeshes.new_from_object()を使うべきと書いてあるが、
-    # それだとシェイプキーが保持されない。
     if isinstance(obj_data, Mesh):
         evaluated_mesh = obj_data.copy()
     else: