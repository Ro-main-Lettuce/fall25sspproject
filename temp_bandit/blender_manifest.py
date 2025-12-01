@@ -41,14 +41,14 @@ def read(cls, blender_manifest: Optional[str] = None) -> ""BlenderManifest"":
 
         version = cls.read_3_tuple_version(blender_manifest, ""version"")
         if version is None:
-            message = ""'version' does not found in blender manifest""
+            message = ""'version' was not found in blender manifest""
             raise ValueError(message)
 
         blender_version_min = cls.read_3_tuple_version(
             blender_manifest, ""blender_version_min""
         )
         if blender_version_min is None:
-            message = ""'blender_version_min' does not found in blender manifest""
+            message = ""'blender_version_min' was not found in blender manifest""
             raise ValueError(message)
 
         return BlenderManifest(