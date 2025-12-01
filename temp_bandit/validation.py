@@ -759,8 +759,8 @@ def detect_errors(
             if not first_person.first_person_bone.bone_name:
                 info_messages.append(
                     pgettext(
-                        ""firstPersonBone is not found. ""
-                        + 'Set VRM HumanBone ""head"" instead automatically.'
+                        ""firstPersonBone was not found. ""
+                        + 'VRM HumanBone ""head"" will be used automatically instead.'
                     )
                 )
 
@@ -818,8 +818,8 @@ def detect_errors(
 
         error_messages.extend(
             pgettext(
-                '""{image_name}"" is not found in file path ""{image_filepath}"". '
-                + ""please load file of it in Blender.""
+                '""{image_name}"" was not found at file path ""{image_filepath}"". '
+                + ""Please load the file in Blender.""
             ).format(image_name=image.name, image_filepath=image.filepath_from_user())
             for image in used_images
             if (