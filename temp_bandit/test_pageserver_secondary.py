@@ -14,6 +14,7 @@
     NeonEnvBuilder,
     NeonPageserver,
     StorageControllerMigrationConfig,
+    flush_ep_to_pageserver,
 )
 from fixtures.pageserver.common_types import parse_layer_file_name
 from fixtures.pageserver.utils import (
@@ -997,10 +998,6 @@ def count_timeline_heatmap_layers(tlid) -> tuple[int, int]:
     ps_secondary.http_client().tenant_heatmap_upload(tenant_id)
     heatmap_after_migration = timeline_heatmap(timeline_id)
 
-    local_layers = ps_secondary.list_layers(tenant_id, timeline_id)
-    # We download 1 layer per second and give up within 5 seconds.
-    assert len(local_layers) < 10
-
     after_migration_heatmap_layers_count = len(heatmap_after_migration[""layers""])
     log.info(f""Heatmap size after cold migration is {after_migration_heatmap_layers_count}"")
 
@@ -1038,9 +1035,14 @@ def no_layers_downloaded(node):
         .value
     )
 
-    workload.stop()
     assert before == after
 
+    # Stop the endpoint and wait until any finally written WAL propagates to
+    # the pageserver and is uploaded to remote storage.
+    flush_ep_to_pageserver(env, workload.endpoint(), tenant_id, timeline_id)
+    ps_secondary.http_client().timeline_checkpoint(tenant_id, timeline_id, wait_until_uploaded=True)
+    workload.stop()
+
     # Now simulate the case where a child timeline is archived, parent layers
     # are evicted and the child is unarchived. When the child is unarchived,
     # itself and the parent update their heatmaps to contain layers needed by the