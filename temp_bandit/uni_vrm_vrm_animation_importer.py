@@ -296,7 +296,7 @@ def import_vrm_animation(context: Context, path: Path, armature: Object) -> set[
 
         translation = node_dict.get(""translation"")
         if isinstance(translation, list) and translation:
-            default_preview_value = translation[0]  # TODO: Matrixだった場合
+            default_preview_value = translation[0]  # TODO: In case of Matrix
             if not isinstance(default_preview_value, (float, int)):
                 default_preview_value = 0.0
         else:
@@ -414,10 +414,10 @@ def import_vrm_animation(context: Context, path: Path, armature: Object) -> set[
                 timestamp,
             )
 
-    # ボーンの状態変更が発生するので、この処理は最後に行う。
-    # hipsにtranslationが割り当てられている場合かつ、hipsが親と
-    # 「use_connect」になっている場合移動アニメーションが反映されないので
-    # 解除する
+    # This process should be done last because bone state changes occur.
+    # If translation is assigned to hips and hips is connected to parent
+    # with ""use_connect"", the movement animation will not be reflected, so
+    # we need to disconnect it
     if node_index_to_translation_keyframes.get(hips_node_index):
         with save_workspace(context, armature, mode=""EDIT""):
             armature_data = armature.data
@@ -570,8 +570,8 @@ def build(
             @ Matrix.Diagonal(scale).to_4x4()
         )
 
-        # TODO: 3要素の場合はオイラー角になるか?
-        # TODO: Matrixだったら分解する
+        # TODO: Is it an Euler angle in the case of 3 elements?
+        # TODO: Decompose if it's a Matrix
 
         child_indices = node_dict.get(""children"")
         if isinstance(child_indices, list):
@@ -743,8 +743,9 @@ def assign_humanoid_keyframe(
                 )
             )
 
-            # TODO: UniVRMはhipsの高さの比で移動量を調整しているように見える。
-            # 仕様には記載が無い。UniVRMのソースコード上でどうなっているかの調査が必要。
+            # TODO: UniVRM seems to adjust the movement amount by the ratio of
+            # hips height. This is not described in the specification.
+            # Investigation of how it works in UniVRM source code is needed.
             rest_world_translation_z = rest_world_matrix.to_translation().z
             if abs(rest_world_translation_z) > 0:
                 world_height_ratio = (