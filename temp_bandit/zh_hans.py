@@ -259,14 +259,14 @@
     + ""直接向 “表面 ”指定其中之一。 输出空材质。。"",
     (
         ""*"",
-        '""{image_name}"" is not found in file path ""{image_filepath}"". '
-        + ""please load file of it in Blender."",
+        '""{image_name}"" was not found at file path ""{image_filepath}"". '
+        + ""Please load the file in Blender."",
     ): '「{image_name}」指定文件路径中的图像文件。「""{image_filepath}""」'
     + ""图像不存在于 请重新加载图像。。"",
     (
         ""*"",
-        ""firstPersonBone is not found. ""
-        + 'Set VRM HumanBone ""head"" instead automatically.',
+        ""firstPersonBone was not found. ""
+        + 'VRM HumanBone ""head"" will be used automatically instead.',
     ): ""firstPersonBone未设置。。""
     + ""自动设置将 VRM humanborn「head」改为 firstPersonBone。。"",
     (