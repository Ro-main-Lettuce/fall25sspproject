@@ -20,16 +20,16 @@ def show_section_header(title):
 
 with timer(""Importing kura modules""):
     # Import the procedural Kura v1 components
-    from kura.v1 import (
+    from kura import (
         summarise_conversations,
         generate_base_clusters_from_conversation_summaries,
         reduce_clusters_from_base_clusters,
         reduce_dimensionality_from_clusters,
         CheckpointManager,
     )
 
-    # Import v1 visualization functions
-    from kura.v1.visualization import (
+    # Import visualization functions
+    from kura.visualization import (
         visualise_clusters_enhanced,
         visualise_clusters_rich,
         visualise_from_checkpoint_manager,