@@ -175,7 +175,7 @@ def update_vrm0_material_property_names(
 
 
 class VrmAddonBoneExtensionPropertyGroup(PropertyGroup):
-    uuid: StringProperty = StringProperty()  # type: ignore[valid-type]
+    uuid: StringProperty()  # type: ignore[valid-type]
 
     (
         axis_translation_enum,