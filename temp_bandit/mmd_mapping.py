@@ -9,6 +9,8 @@
 
 logger = get_logger(__name__)
 
+# Mapping table for MMD (MikuMikuDance) bone names to VRM human bone specifications.
+# These Japanese bone names are standard MMD naming conventions and should be preserved.
 MMD_BONE_NAME_AND_HUMAN_BONE_SPECIFICATION_PAIRS: Final[
     Sequence[tuple[str, HumanBoneSpecification]]
 ] = [