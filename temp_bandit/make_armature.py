@@ -37,15 +37,15 @@ class ICYP_OT_make_armature(Operator):
         default=False
     )
 
-    # 身長 at meter
+    # Height in meters
     tall: FloatProperty(  # type: ignore[valid-type]
         default=1.70,
         min=0.3,
         step=1,
         name=""Bone tall"",
     )
 
-    # 頭身
+    # Head-to-body ratio
     head_ratio: FloatProperty(  # type: ignore[valid-type]
         default=8.0,
         min=4,
@@ -61,17 +61,17 @@ class ICYP_OT_make_armature(Operator):
         description=""height per heads"",
     )
 
-    # 足-胴比率:0:子供、1:大人 に近くなる(低等身で有効)
+    # Leg-to-torso ratio: 0: child-like, 1: adult-like (effective for low head count)
     aging_ratio: FloatProperty(  # type: ignore[valid-type]
         default=0.5, min=0, max=1, step=10
     )
 
-    # 目の奥み
+    # Eye depth
     eye_depth: FloatProperty(  # type: ignore[valid-type]
         default=-0.03, min=-0.1, max=0, step=1
     )
 
-    # 肩幅
+    # Shoulder width
     shoulder_in_width: FloatProperty(  # type: ignore[valid-type]
         default=0.05,
         min=0.01,
@@ -86,12 +86,12 @@ class ICYP_OT_make_armature(Operator):
         description=""shoulder roll position"",
     )
 
-    # 腕長さ率
+    # Arm length ratio
     arm_length_ratio: FloatProperty(  # type: ignore[valid-type]
         default=1, min=0.5, step=1
     )
 
-    # 手
+    # Hand
     hand_ratio: FloatProperty(  # type: ignore[valid-type]
         default=1, min=0.5, max=2.0, step=5
     )
@@ -115,9 +115,9 @@ class ICYP_OT_make_armature(Operator):
     nail_bone: BoolProperty(  # type: ignore[valid-type]
         default=False,
         description=""may need for finger collider"",
-    )  # 指先の当たり判定として必要
+    )  # Needed for fingertip collision detection
 
-    # 足
+    # Foot
     leg_length_ratio: FloatProperty(  # type: ignore[valid-type]
         default=0.5,
         min=0.3,
@@ -316,8 +316,9 @@ def fingers(
         # bone_type = ""leg"" or ""arm"" for roll setting
 
         head_size = self.head_size()
-        # down side (前は8頭身の時の股上/股下の股下側割合、
-        # 後ろは4頭身のときの〃を年齢具合で線形補完)(股上高めにすると破綻する)
+        # down side (previously the lower leg ratio of upper leg/lower leg for
+        # 8-head proportions, later linearly interpolated with age factor for
+        # 4-head proportions)(breaks if upper leg is too high)
         eight_upside_ratio, four_upside_ratio = (
             1 - self.leg_length_ratio,
             (2.5 / 4) * (1 - self.aging_ratio)
@@ -327,22 +328,22 @@ def fingers(
             eight_upside_ratio * (1 - (8 - self.head_ratio) / 4)
             + four_upside_ratio * (8 - self.head_ratio) / 4
         )
-        # 体幹
-        # 股間
+        # Torso
+        # Groin
         body_separate = self.tall * (1 - hip_up_down_ratio)
-        # 首の長さ
+        # Neck length
         neck_len = head_size * 2 / 3
-        # 仙骨(骨盤脊柱基部)
+        # Sacrum (pelvic spine base)
         hips_tall = body_separate + head_size * 3 / 4
-        # 胸椎・spineの全長 #首の1/3は顎の後ろに隠れてる
+        # Thoracic spine total length # 1/3 of neck is hidden behind the jaw
         backbone_len = self.tall - hips_tall - head_size - neck_len / 2
-        # TODO: 胸椎と脊椎の割合の確認
-        # 脊椎の基部に位置する主となる屈曲点と、胸郭基部に位置するもうひとつの屈曲点
+        # TODO: Verify the ratio of thoracic spine to vertebrae
+        # Main flexion point located at the base of the spine, and another flexion point located at the base of the thoracic cage
         # by Humanoid Doc
         spine_len = backbone_len * 5 / 17
 
         root = bone_add(armature_data, ""root"", Vector((0, 0, 0)), Vector((0, 0, 0.3)))
-        # 仙骨基部
+        # Sacrum base
         hips = bone_add(
             armature_data,
             ""hips"",
@@ -351,11 +352,11 @@ def fingers(
             root,
             roll=0,
         )
-        # 骨盤基部->胸郭基部
+        # Pelvic base -> Thoracic cage base
         spine = bone_add(
             armature_data, ""spine"", hips.tail, z_add(hips.tail, spine_len), hips, roll=0
         )
-        # 胸郭基部->首元
+        # Thoracic cage base -> Neck base
         chest = bone_add(
             armature_data,
             ""chest"",