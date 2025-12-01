@@ -13,7 +13,6 @@
 
 @dataclass(frozen=True)
 class SavedWorkspace:
-    # yield前後で消えるかもしれないオブジェクトを含まないように注意する
     cursor_matrix: Matrix
     previous_object_name: Optional[str]
     previous_object_mode: Optional[str]
@@ -24,45 +23,33 @@ class SavedWorkspace:
 def enter_save_workspace(
     context: Context, obj: Optional[Object] = None, *, mode: str = ""OBJECT""
 ) -> SavedWorkspace:
-    # 3Dカーソルの位置を保存
     cursor_matrix = context.scene.cursor.matrix.copy()
 
     previous_object_name = None
     previous_object_mode = None
     previous_object = context.view_layer.objects.active
     if previous_object:
-        # yield後にprevious_objectが消える場合がある。
-        # いちおうinternをしておくが、不要かもしれない。
         previous_object_name = sys.intern(previous_object.name)
         previous_object_mode = sys.intern(previous_object.mode)
 
-        # obj引数が渡された場合モードを""OBJECT""にする。モードがそのままだと、
-        # アクティブなオブジェクトを変更できないことがある
         if previous_object != obj and previous_object_mode != ""OBJECT"":
             previous_object_hide_viewport = previous_object.hide_viewport
             if previous_object_hide_viewport:
-                # hide_viewportがTrueの場合、そのままだとmode_setに失敗する可能性がある
                 previous_object.hide_viewport = False
             bpy.ops.object.mode_set(mode=""OBJECT"")
             if previous_object.hide_viewport != previous_object_hide_viewport:
                 previous_object.hide_viewport = previous_object_hide_viewport
 
-    # オブジェクトを渡された場合、それをアクティブにする
     if obj is not None:
         context.view_layer.objects.active = obj
         context.view_layer.update()
 
     active_object_name = None
     active_object_hide_viewport = False
-    # アクティブなオブジェクトのモードを変更する
     active_object = context.view_layer.objects.active
     if active_object:
-        # yield後にactive_objectが消える場合がある。
-        # いちおうinternをしておくが、不要かもしれない。
         active_object_name = sys.intern(active_object.name)
         active_object_hide_viewport = active_object.hide_viewport
-        # hide_viewportがTrueの場合、そのままだとmode_setに失敗する可能性がある
-        # 現在はモードを変更しない場合も強制的に表示状態にしてあるが、不適切かも
         if active_object_hide_viewport:
             active_object.hide_viewport = False
         if active_object.mode != mode:
@@ -90,8 +77,6 @@ def exit_save_workspace(context: Context, saved_workspace: SavedWorkspace) -> No
 
     current_active_object = context.view_layer.objects.active
 
-    # 現在アクティブなオブジェクトのモードを""OBJECT""にする。モードがそのままだと、
-    # アクティブなオブジェクトを変更できないことがある
     if (
         current_active_object
         and current_active_object != previous_object
@@ -104,13 +89,11 @@ def exit_save_workspace(context: Context, saved_workspace: SavedWorkspace) -> No
         if current_active_object.hide_viewport != current_active_object_hide_viewport:
             current_active_object.hide_viewport = current_active_object_hide_viewport
 
-    # アクティブにしたオブジェクトのhide_viewportを戻す
     if active_object_name is not None:
         active_object = context.blend_data.objects.get(active_object_name)
         if active_object and active_object.hide_viewport != active_object_hide_viewport:
             active_object.hide_viewport = active_object_hide_viewport
 
-    # もともとアクティブだったオブジェクトに戻す
     previous_object = None
     if previous_object_name is not None:
         previous_object = context.blend_data.objects.get(previous_object_name)
@@ -119,22 +102,18 @@ def exit_save_workspace(context: Context, saved_workspace: SavedWorkspace) -> No
         context.view_layer.objects.active = previous_object
         context.view_layer.update()
 
-    # もともとアクティブだったオブジェクトのモードを戻す
     if (
         previous_object
         and previous_object_mode is not None
         and previous_object_mode != previous_object.mode
     ):
-        # hide_viewportがTrueの場合、そのままだとmode_setに失敗する可能性がある
-        # mode_setが完了してからhide_viewportを復元する
         previous_object_hide_viewport = previous_object.hide_viewport
         if previous_object_hide_viewport:
             previous_object.hide_viewport = False
         bpy.ops.object.mode_set(mode=previous_object_mode)
         if previous_object.hide_viewport != previous_object_hide_viewport:
             previous_object.hide_viewport = previous_object_hide_viewport
 
-    # 3Dカーソルをの位置をもとに戻す
     context.scene.cursor.matrix = cursor_matrix
 
 
@@ -165,8 +144,6 @@ def wm_append_without_library(
     """"""
     # https://projects.blender.org/blender/blender/src/tag/v2.93.18/source/blender/windowmanager/intern/wm_files_link.c#L85-L90
     with save_workspace(context):
-        # ライブラリの追加検知用のポインタリスト。
-        # 追加検知のみに用いる。特に、デリファレンスは危険なので行わないように注意する。
         existing_library_pointers: list[int] = [
             library.as_pointer() for library in context.blend_data.libraries
         ]