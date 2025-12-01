@@ -391,7 +391,7 @@ def draw_vrm0_humanoid_layout(
     draw_vrm0_humanoid_required_bones_layout(armature, armature_box.box(), split_factor)
     draw_vrm0_humanoid_optional_bones_layout(armature, armature_box.box(), split_factor)
 
-    layout.label(text=""Arm"", icon=""VIEW_PAN"", translate=False)  # TODO: 翻訳
+    layout.label(text=""Arm"", icon=""VIEW_PAN"", translate=False)  # TODO: Translation
     layout.prop(
         humanoid,
         ""arm_stretch"",