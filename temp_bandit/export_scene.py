@@ -279,7 +279,7 @@ def export_vrm(
 
     with save_workspace(
         context,
-        # アクティブオブジェクト変更しても元に戻せるようにする
+        # Allow restoring after changing active object
         armature_object,
     ):
         if armature_object:
@@ -321,7 +321,7 @@ def export_vrm(
         if armature_object.users:
             logger.warning(""Failed to remove temporary armature"")
         else:
-            # アクティブオブジェクトから外れた後にremoveする
+            # Remove after deactivating from active object
             context.blend_data.objects.remove(armature_object)
 
     return {""FINISHED""}