@@ -1,4 +1,5 @@
 import json
+import math
 import sys
 from pathlib import Path
 
@@ -12,13 +13,12 @@ def load_json_with_fallback(path: Path):
         print(f""⚠️ Missing: {path}"")
         return {}
     try:
-        with open(path, encoding=""utf-8"") as f:
+        with open(path, encoding='utf-8') as f:
             return json.load(f)
     except UnicodeDecodeError:
-        with open(path, encoding=""shift_jis"") as f:
+        with open(path, encoding='shift_jis') as f:
             return json.load(f)
 
-
 # -----------------------------
 # 引数でディレクトリ指定（例: python generate_csv.py 2）
 # -----------------------------
@@ -43,7 +43,6 @@ def load_json_with_fallback(path: Path):
 OUT_CLUSTER_CSV = output_dir / ""cluster_evaluation.csv""
 OUT_COMMENT_CSV = output_dir / ""comment_evaluation.csv""
 
-
 # -----------------------------
 # クラスタ単位の出力
 # -----------------------------
@@ -54,18 +53,12 @@ def generate_cluster_csv():
         if ""id"" in df.columns:
             df = df.rename(columns={""id"": ""cluster_id""})
         else:
-            raise KeyError(
-                ""クラスタID列が見つかりません（'cluster_id' または 'id' が必要です）""
-            )
+            raise KeyError(""クラスタID列が見つかりません（'cluster_id' または 'id' が必要です）"")
 
     llm_scores_l1 = load_json_with_fallback(EVAL_LLM_JSON_L1)
     llm_scores_l2 = load_json_with_fallback(EVAL_LLM_JSON_L2)
-    umap_scores_l1 = load_json_with_fallback(SIL_UMAP_CLUSTER_JSON_L1).get(
-        ""clusters"", {}
-    )
-    umap_scores_l2 = load_json_with_fallback(SIL_UMAP_CLUSTER_JSON_L2).get(
-        ""clusters"", {}
-    )
+    umap_scores_l1 = load_json_with_fallback(SIL_UMAP_CLUSTER_JSON_L1).get(""clusters"", {})
+    umap_scores_l2 = load_json_with_fallback(SIL_UMAP_CLUSTER_JSON_L2).get(""clusters"", {})
 
     llm_scores = {**llm_scores_l1, **llm_scores_l2}
     umap_scores = {**umap_scores_l1, **umap_scores_l2}
@@ -79,50 +72,25 @@ def get_umap_metric(cid, key):
     df[""clarity""] = df[""cluster_id""].map(lambda x: get_llm_value(x, ""clarity""))
     df[""coherence""] = df[""cluster_id""].map(lambda x: get_llm_value(x, ""coherence""))
     df[""consistency""] = df[""cluster_id""].map(lambda x: get_llm_value(x, ""consistency""))
-    df[""distinctiveness""] = df[""cluster_id""].map(
-        lambda x: get_llm_value(x, ""distinctiveness"")
-    )
+    df[""distinctiveness""] = df[""cluster_id""].map(lambda x: get_llm_value(x, ""distinctiveness""))
     df[""llm_comment""] = df[""cluster_id""].map(lambda x: get_llm_value(x, ""comment""))
 
     df[""silhouette""] = df[""cluster_id""].map(lambda x: get_umap_metric(x, ""silhouette""))
-    df[""silhouette_score""] = df[""cluster_id""].map(
-        lambda x: get_umap_metric(x, ""silhouette_score"")
-    )
+    df[""silhouette_score""] = df[""cluster_id""].map(lambda x: get_umap_metric(x, ""silhouette_score""))
     df[""centroid""] = df[""cluster_id""].map(lambda x: get_umap_metric(x, ""centroid_dist""))
-    df[""centroid_score""] = df[""cluster_id""].map(
-        lambda x: get_umap_metric(x, ""centroid_score"")
-    )
+    df[""centroid_score""] = df[""cluster_id""].map(lambda x: get_umap_metric(x, ""centroid_score""))
     df[""nearest""] = df[""cluster_id""].map(lambda x: get_umap_metric(x, ""nearest_dist""))
-    df[""nearest_score""] = df[""cluster_id""].map(
-        lambda x: get_umap_metric(x, ""nearest_score"")
-    )
+    df[""nearest_score""] = df[""cluster_id""].map(lambda x: get_umap_metric(x, ""nearest_score""))
 
     desired_order = [
-        ""level"",
-        ""cluster_id"",
-        ""label"",
-        ""description"",
-        ""value"",
-        ""parent"",
-        ""density"",
-        ""density_rank"",
-        ""density_rank_percentile"",
-        ""clarity"",
-        ""coherence"",
-        ""consistency"",
-        ""distinctiveness"",
-        ""llm_comment"",
-        ""silhouette"",
-        ""silhouette_score"",
-        ""centroid"",
-        ""centroid_score"",
-        ""nearest"",
-        ""nearest_score"",
+        ""level"", ""cluster_id"", ""label"", ""description"", ""value"", ""parent"", ""density"",
+        ""density_rank"", ""density_rank_percentile"",
+        ""clarity"", ""coherence"", ""consistency"", ""distinctiveness"", ""llm_comment"",
+        ""silhouette"", ""silhouette_score"", ""centroid"", ""centroid_score"", ""nearest"", ""nearest_score""
     ]
     df_out = df[[col for col in desired_order if col in df.columns]]
     df_out.to_csv(OUT_CLUSTER_CSV, index=False)
 
-
 # -----------------------------
 # 意見単位の出力
 # -----------------------------
@@ -148,14 +116,13 @@ def generate_comment_csv():
                 ""centroid"": p.get(""centroid_dist""),
                 ""centroid_score"": p.get(""centroid_score""),
                 ""nearest"": p.get(""nearest_dist""),
-                ""nearest_score"": p.get(""nearest_score""),
+                ""nearest_score"": p.get(""nearest_score"")
             }
             rows.append(row)
 
     df = pd.DataFrame(rows)
     df.to_csv(OUT_COMMENT_CSV, index=False)
 
-
 # -----------------------------
 if __name__ == ""__main__"":
     generate_cluster_csv()