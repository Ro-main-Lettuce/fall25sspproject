@@ -179,7 +179,7 @@ def validate_blend_file_compatibility(context: Context) -> None:
 
     if not state.blend_file_compatibility_warning_shown:
         state.blend_file_compatibility_warning_shown = True
-        # Blender 4.2.0ではtimerで実行しないとダイアログが自動で消えるのでタイマーを使う
+        # Use timer because dialog disappears automatically if not executed with timer in Blender 4.2.0
         bpy.app.timers.register(
             functools.partial(
                 show_blend_file_compatibility_warning,
@@ -199,12 +199,12 @@ def show_blend_file_compatibility_warning(file_version: str, app_version: str) -
 
 
 def validate_blend_file_addon_compatibility(context: Context) -> None:
-    """"""新しいVRMアドオンで作成されたファイルを古いVRMアドオンで編集しようとした場合に警告をする.""""""
+    """"""Warn when attempting to edit a file created with a newer VRM add-on using an older VRM add-on.""""""
     if not context.blend_data.filepath:
         return
     installed_addon_version = get_addon_version()
 
-    # TODO: これはSceneあたりにバージョンを生やしたほうが良いかも
+    # TODO: It might be better to store the version in Scene or similar
     up_to_date = True
     file_addon_version: tuple[int, ...] = (0, 0, 0)
     for armature in context.blend_data.armatures:
@@ -226,7 +226,7 @@ def validate_blend_file_addon_compatibility(context: Context) -> None:
 
     if not state.blend_file_compatibility_warning_shown:
         state.blend_file_compatibility_warning_shown = True
-        # Blender 4.2.0ではtimerで実行しないとダイアログが自動で消えるのでタイマーを使う
+        # Use timer because dialog disappears automatically if not executed with timer in Blender 4.2.0
         bpy.app.timers.register(
             functools.partial(
                 show_blend_file_addon_compatibility_warning,