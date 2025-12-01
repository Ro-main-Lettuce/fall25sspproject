@@ -290,14 +290,14 @@
     + ""いずれかを直接「サーフェス」に指定してください。空のマテリアルを出力します。"",
     (
         ""*"",
-        '""{image_name}"" is not found in file path ""{image_filepath}"". '
-        + ""please load file of it in Blender."",
+        '""{image_name}"" was not found at file path ""{image_filepath}"". '
+        + ""Please load the file in Blender."",
     ): '「{image_name}」の画像ファイルが指定ファイルパス「""{image_filepath}""」'
     + ""に存在しません。画像を読み込み直してください。"",
     (
         ""*"",
-        ""firstPersonBone is not found. ""
-        + 'Set VRM HumanBone ""head"" instead automatically.',
+        ""firstPersonBone was not found. ""
+        + 'VRM HumanBone ""head"" will be used automatically instead.',
     ): ""firstPersonBoneが設定されていません。""
     + ""代わりにfirstPersonBoneとしてVRMヒューマンボーン「head」を自動で設定します。"",
     (