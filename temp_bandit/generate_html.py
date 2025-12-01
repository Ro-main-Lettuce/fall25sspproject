@@ -45,12 +45,8 @@ def generate_html(slug: str, input_dir: Path, output_dir: Path, template_dir: Pa
     distinctiveness_comment1 = llm_scores_l1.pop(""distinctiveness_comment"", None)
     distinctiveness_comment2 = llm_scores_l2.pop(""distinctiveness_comment"", None)
 
-    silhouette_umap = load_json(
-        base_input / ""silhouette_umap_level1_clusters.json""
-    ).get(""clusters"", {})
-    silhouette_umap_lv2 = load_json(
-        base_input / ""silhouette_umap_level2_clusters.json""
-    ).get(""clusters"", {})
+    silhouette_umap = load_json(base_input / ""silhouette_umap_level1_clusters.json"").get(""clusters"", {})
+    silhouette_umap_lv2 = load_json(base_input / ""silhouette_umap_level2_clusters.json"").get(""clusters"", {})
 
     umap_points = load_json(base_input / ""silhouette_umap_level2_points.json"")
     if not umap_points:
@@ -66,10 +62,10 @@ def generate_html(slug: str, input_dir: Path, output_dir: Path, template_dir: Pa
                 ""centroid"": ump.get(""centroid_dist""),
                 ""centroid_score"": ump.get(""centroid_score""),
                 ""nearest"": ump.get(""nearest_dist""),
-                ""nearest_score"": ump.get(""nearest_score""),
+                ""nearest_score"": ump.get(""nearest_score"")
             }
         }
-    {c[""id""]: c for c in result_data[""clusters""]}
+    cluster_by_id = {c[""id""]: c for c in result_data[""clusters""]}
     cluster_children = {}
     for c in result_data[""clusters""]:
         parent = c.get(""parent"")
@@ -93,36 +89,22 @@ def build_cluster_tree(cluster):
         umap = silhouette_umap.get(cid) if level == 1 else silhouette_umap_lv2.get(cid)
 
         cluster[""scores""] = {
-            ""clarity"": {
-                ""raw"": llm.get(""clarity""),
-                ""scaled"": safe_int(llm.get(""clarity"")),
-            },
-            ""coherence"": {
-                ""raw"": llm.get(""coherence""),
-                ""scaled"": safe_int(llm.get(""coherence"")),
-            },
-            ""consistency"": {
-                ""raw"": llm.get(""consistency""),
-                ""scaled"": safe_int(llm.get(""consistency"")),
-            },
-            ""distinctiveness"": {
-                ""raw"": llm.get(""distinctiveness""),
-                ""scaled"": safe_int(llm.get(""distinctiveness"")),
-            },
+            ""clarity"": {""raw"": llm.get(""clarity""), ""scaled"": safe_int(llm.get(""clarity""))},
+            ""coherence"": {""raw"": llm.get(""coherence""), ""scaled"": safe_int(llm.get(""coherence""))},
+            ""consistency"": {""raw"": llm.get(""consistency""), ""scaled"": safe_int(llm.get(""consistency""))},
+            ""distinctiveness"": {""raw"": llm.get(""distinctiveness""), ""scaled"": safe_int(llm.get(""distinctiveness""))},
             ""umap"": {
                 ""raw"": umap.get(""silhouette"") if umap else None,
                 ""scaled"": umap.get(""silhouette_score"") if umap else None,
                 ""centroid"": umap.get(""centroid_dist"") if umap else None,
                 ""centroid_score"": umap.get(""centroid_score"") if umap else None,
                 ""nearest"": umap.get(""nearest_dist"") if umap else None,
-                ""nearest_score"": umap.get(""nearest_score"") if umap else None,
-            },
+                ""nearest_score"": umap.get(""nearest_score"") if umap else None
+            }
         }
 
         cluster[""silhouette_umap""] = umap
-        cluster[""children""] = [
-            build_cluster_tree(child) for child in cluster_children.get(cid, [])
-        ]
+        cluster[""children""] = [build_cluster_tree(child) for child in cluster_children.get(cid, [])]
         return cluster
 
     level1_clusters = [c for c in result_data[""clusters""] if c.get(""level"") == 1]
@@ -131,12 +113,8 @@ def build_cluster_tree(cluster):
     result_data[""llm_avg""] = {
         ""clarity"": mean([safe_int(c[""llm""].get(""clarity"")) for c in cluster_tree]),
         ""coherence"": mean([safe_int(c[""llm""].get(""coherence"")) for c in cluster_tree]),
-        ""consistency"": mean(
-            [safe_int(c[""llm""].get(""consistency"")) for c in cluster_tree]
-        ),
-        ""distinctiveness"": mean(
-            [safe_int(c[""llm""].get(""distinctiveness"")) for c in cluster_tree]
-        ),
+        ""consistency"": mean([safe_int(c[""llm""].get(""consistency"")) for c in cluster_tree]),
+        ""distinctiveness"": mean([safe_int(c[""llm""].get(""distinctiveness"")) for c in cluster_tree]),
     }
 
     result_data[""llm_avg_scaled""] = {
@@ -147,79 +125,37 @@ def build_cluster_tree(cluster):
     }
 
     result_data[""silhouette_umap_avg""] = {
-        ""silhouette"": mean(
-            [
-                v.get(""silhouette"")
-                for v in silhouette_umap.values()
-                if isinstance(v, dict)
-            ]
-        ),
-        ""silhouette_score"": mean(
-            [
-                v.get(""silhouette_score"")
-                for v in silhouette_umap.values()
-                if isinstance(v, dict)
-            ]
-        ),
-        ""centroid_dist"": mean(
-            [
-                v.get(""centroid_dist"")
-                for v in silhouette_umap.values()
-                if isinstance(v, dict)
-            ]
-        ),
-        ""centroid_score"": mean(
-            [
-                v.get(""centroid_score"")
-                for v in silhouette_umap.values()
-                if isinstance(v, dict)
-            ]
-        ),
-        ""nearest_dist"": mean(
-            [
-                v.get(""nearest_dist"")
-                for v in silhouette_umap.values()
-                if isinstance(v, dict)
-            ]
-        ),
-        ""nearest_score"": mean(
-            [
-                v.get(""nearest_score"")
-                for v in silhouette_umap.values()
-                if isinstance(v, dict)
-            ]
-        ),
+        ""silhouette"": mean([v.get(""silhouette"") for v in silhouette_umap.values() if isinstance(v, dict)]),
+        ""silhouette_score"": mean([v.get(""silhouette_score"") for v in silhouette_umap.values() if isinstance(v, dict)]),
+        ""centroid_dist"": mean([v.get(""centroid_dist"") for v in silhouette_umap.values() if isinstance(v, dict)]),
+        ""centroid_score"": mean([v.get(""centroid_score"") for v in silhouette_umap.values() if isinstance(v, dict)]),
+        ""nearest_dist"": mean([v.get(""nearest_dist"") for v in silhouette_umap.values() if isinstance(v, dict)]),
+        ""nearest_score"": mean([v.get(""nearest_score"") for v in silhouette_umap.values() if isinstance(v, dict)]),
     }
 
     result_data[""silhouette_umap_avg_scaled""] = {
-        ""silhouette_score"": round(
-            result_data[""silhouette_umap_avg""].get(""silhouette_score"")
-        ),
-        ""centroid_score"": round(
-            result_data[""silhouette_umap_avg""].get(""centroid_score"")
-        ),
+        ""silhouette_score"": round(result_data[""silhouette_umap_avg""].get(""silhouette_score"")),
+        ""centroid_score"": round(result_data[""silhouette_umap_avg""].get(""centroid_score"")),
         ""nearest_score"": round(result_data[""silhouette_umap_avg""].get(""nearest_score"")),
     }
 
     color_map = {}
     for i, c in enumerate(level1_clusters):
         hue = (i * 0.14) % 1.0
         rgb = colorsys.hsv_to_rgb(hue, 0.6, 0.7)
-        hex_color = ""#{:02x}{:02x}{:02x}"".format(
-            int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)
-        )
+        hex_color = '#{:02x}{:02x}{:02x}'.format(int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))
         color_map[c[""id""]] = hex_color
 
     env = Environment(loader=FileSystemLoader(str(template_dir)))
-    env.tests[""search""] = lambda value, sub: sub in value
+    env.tests['search'] = lambda value, sub: sub in value
     template = env.get_template(""report_template.html"")
     html = template.render(
         result=result_data,
         cluster_tree=cluster_tree,
         umap_thresholds=UMAP_THRESHOLDS,
         color_map=color_map,
-        distinctiveness_comment1=distinctiveness_comment1,
-        distinctiveness_comment2=distinctiveness_comment2,
+        distinctiveness_comment1=distinctiveness_comment1, 
+        distinctiveness_comment2=distinctiveness_comment2,  
     )
 
     out_path = base_output / ""report.html""
@@ -237,7 +173,7 @@ def main():
         slug=slug,
         input_dir=Path(""inputs""),
         output_dir=Path(""outputs""),
-        template_dir=Path(""templates""),
+        template_dir=Path(""templates"")
     )
 
 