@@ -3,12 +3,40 @@
 import json
 from collections import defaultdict
 from pathlib import Path
-from typing import TypedDict
+from typing import Any, TypedDict
 
+import numpy as np
 import pandas as pd
 
 ROOT_DIR = Path(__file__).parent.parent.parent.parent
 CONFIG_DIR = ROOT_DIR / ""scatter"" / ""pipeline"" / ""configs""
+PIPELINE_DIR = ROOT_DIR / ""broadlistening"" / ""pipeline""
+
+
+def json_serialize_numpy(obj: Any) -> Any:
+    """"""
+    Recursively convert NumPy data types to native Python types for JSON serialization.
+
+    Args:
+        obj: Any Python object which might contain NumPy data types
+
+    Returns:
+        The same object structure with NumPy types converted to Python native types
+    """"""
+    if isinstance(obj, np.integer):
+        return int(obj)
+    elif isinstance(obj, np.floating):
+        return float(obj)
+    elif isinstance(obj, np.ndarray):
+        return obj.tolist()
+    elif isinstance(obj, dict):
+        return {k: json_serialize_numpy(v) for k, v in obj.items()}
+    elif isinstance(obj, list):
+        return [json_serialize_numpy(item) for item in obj]
+    elif isinstance(obj, tuple):
+        return tuple(json_serialize_numpy(item) for item in obj)
+    else:
+        return obj
 
 
 class Argument(TypedDict):
@@ -19,6 +47,7 @@ class Argument(TypedDict):
     y: float
     p: float
     cluster_ids: list[str]
+    attributes: dict[str, str] | None
 
 
 class Cluster(TypedDict):
@@ -31,58 +60,67 @@ class Cluster(TypedDict):
     density_rank_percentile: float | None
 
 
-def hierarchical_aggregation(config):
-    path = f""outputs/{config['output_dir']}/hierarchical_result.json""
-    results = {
-        ""arguments"": [],
-        ""clusters"": [],
-        ""comments"": {},
-        ""propertyMap"": {},
-        ""translations"": {},
-        ""overview"": """",
-        ""config"": config,
-    }
-
-    arguments = pd.read_csv(f""outputs/{config['output_dir']}/args.csv"")
-    arguments.set_index(""arg-id"", inplace=True)
-    arg_num = len(arguments)
-    relation_df = pd.read_csv(f""outputs/{config['output_dir']}/relations.csv"")
-    comments = pd.read_csv(f""inputs/{config['input']}.csv"")
-    clusters = pd.read_csv(f""outputs/{config['output_dir']}/hierarchical_clusters.csv"")
-    labels = pd.read_csv(f""outputs/{config['output_dir']}/hierarchical_merge_labels.csv"")
-
-    hidden_properties_map: dict[str, list[str]] = config[""hierarchical_aggregation""][""hidden_properties""]
-
-    results[""arguments""] = _build_arguments(clusters)
-    results[""clusters""] = _build_cluster_value(labels, arg_num)
-    # NOTE: 属性に応じたコメントフィルタ機能が実装されておらず、全てのコメントが含まれてしまうので、コメントアウト
-    # results[""comments""] = _build_comments_value(
-    #     comments, arguments, hidden_properties_map
-    # )
-    results[""comment_num""] = len(comments)
-    results[""translations""] = _build_translations(config)
-    # 属性情報のカラムは、元データに対して指定したカラムとclassificationするカテゴリを合わせたもの
-    results[""propertyMap""] = _build_property_map(arguments, hidden_properties_map, config)
-
-    with open(f""outputs/{config['output_dir']}/hierarchical_overview.txt"") as f:
-        overview = f.read()
-    print(""overview"")
-    print(overview)
-    results[""overview""] = overview
-
-    with open(path, ""w"") as file:
-        json.dump(results, file, indent=2, ensure_ascii=False)
-    # TODO: サンプリングロジックを実装したいが、現状は全件抽出
-    create_custom_intro(config)
-    if config[""is_pubcom""]:
-        add_original_comments(labels, arguments, relation_df, clusters, config)
+def hierarchical_aggregation(config) -> bool:
+    try:
+        path = f""outputs/{config['output_dir']}/hierarchical_result.json""
+        results = {
+            ""arguments"": [],
+            ""clusters"": [],
+            ""comments"": {},
+            ""propertyMap"": {},
+            ""translations"": {},
+            ""overview"": """",
+            ""config"": config,
+        }
+
+        arguments = pd.read_csv(f""outputs/{config['output_dir']}/args.csv"")
+        arguments.set_index(""arg-id"", inplace=True)
+        arg_num = len(arguments)
+        relation_df = pd.read_csv(f""outputs/{config['output_dir']}/relations.csv"")
+        comments = pd.read_csv(f""inputs/{config['input']}.csv"")
+        clusters = pd.read_csv(f""outputs/{config['output_dir']}/hierarchical_clusters.csv"")
+        labels = pd.read_csv(f""outputs/{config['output_dir']}/hierarchical_merge_labels.csv"")
+
+        hidden_properties_map: dict[str, list[str]] = config[""hierarchical_aggregation""][""hidden_properties""]
+
+        results[""arguments""] = _build_arguments(clusters, comments, relation_df)
+        results[""clusters""] = _build_cluster_value(labels, arg_num)
+
+        # results[""comments""] = _build_comments_value(
+        #     comments, arguments, hidden_properties_map
+        # )
+        results[""comment_num""] = len(comments)
+        results[""translations""] = _build_translations(config)
+        # 属性情報のカラムは、元データに対して指定したカラムとclassificationするカテゴリを合わせたもの
+        results[""propertyMap""] = _build_property_map(arguments, comments, hidden_properties_map, config)
+
+        with open(f""outputs/{config['output_dir']}/hierarchical_overview.txt"") as f:
+            overview = f.read()
+        print(""overview"")
+        print(overview)
+        results[""overview""] = overview
+
+        # Convert non-serializable NumPy types to native Python types
+        results = json_serialize_numpy(results)
+
+        with open(path, ""w"") as file:
+            json.dump(results, file, indent=2, ensure_ascii=False)
+        # TODO: サンプリングロジックを実装したいが、現状は全件抽出
+        create_custom_intro(config)
+        if config[""is_pubcom""]:
+            add_original_comments(labels, arguments, relation_df, clusters, config)
+        return True
+    except Exception as e:
+        print(""error"")
+        print(e)
+        return False
 
 
 def create_custom_intro(config):
     dataset = config[""output_dir""]
-    args_path = f""outputs/{dataset}/args.csv""
-    comments = pd.read_csv(f""inputs/{config['input']}.csv"")
-    result_path = f""outputs/{dataset}/hierarchical_result.json""
+    args_path = PIPELINE_DIR / f""outputs/{dataset}/args.csv""
+    comments = pd.read_csv(PIPELINE_DIR / f""inputs/{config['input']}.csv"")
+    result_path = PIPELINE_DIR / f""outputs/{dataset}/hierarchical_result.json""
 
     input_count = len(comments)
     args_count = len(pd.read_csv(args_path))
@@ -120,7 +158,7 @@ def add_original_comments(labels, arguments, relation_df, clusters, config):
     merged = merged.merge(relation_df, on=""arg-id"", how=""left"")
 
     # 元コメント取得
-    comments = pd.read_csv(f""inputs/{config['input']}.csv"")
+    comments = pd.read_csv(PIPELINE_DIR / f""inputs/{config['input']}.csv"")
     comments[""comment-id""] = comments[""comment-id""].astype(str)
     merged[""comment-id""] = merged[""comment-id""].astype(str)
 
@@ -129,10 +167,23 @@ def add_original_comments(labels, arguments, relation_df, clusters, config):
 
     # 必要カラムのみ整形
     final_cols = [""comment-id"", ""comment-body"", ""arg-id"", ""argument"", ""cluster-level-1-id"", ""category_label""]
-    for col in [""source"", ""url""]:
+
+    # 基本カラム
+    for col in [""x"", ""y"", ""source"", ""url""]:
         if col in comments.columns:
             final_cols.append(col)
 
+    # 属性カラムを追加
+    attribute_columns = []
+    for col in comments.columns:
+        # attributeプレフィックスが付いたカラムを探す
+        if col.startswith(""attribute_""):
+            attribute_columns.append(col)
+            final_cols.append(col)
+
+    print(f""属性カラム検出: {attribute_columns}"")
+
+    # 必要なカラムだけ選択
     final_df = final_df[final_cols]
     final_df = final_df.rename(
         columns={
@@ -145,25 +196,77 @@ def add_original_comments(labels, arguments, relation_df, clusters, config):
     )
 
     # 保存
-    final_df.to_csv(f""outputs/{config['output_dir']}/final_result_with_comments.csv"", index=False)
+    final_df.to_csv(PIPELINE_DIR / f""outputs/{config['output_dir']}/final_result_with_comments.csv"", index=False)
+
 
+def _build_arguments(clusters: pd.DataFrame, comments: pd.DataFrame, relation_df: pd.DataFrame) -> list[Argument]:
+    """"""
+    Build the arguments list including attribute information from original comments
 
-def _build_arguments(clusters: pd.DataFrame) -> list[Argument]:
+    Args:
+        clusters: DataFrame containing cluster information for each argument
+        comments: DataFrame containing original comments with attribute columns
+        relation_df: DataFrame relating arguments to original comments
+    """"""
     cluster_columns = [col for col in clusters.columns if col.startswith(""cluster-level-"") and ""id"" in col]
 
+    # Prepare for merging with original comments to get attributes
+    comments_copy = comments.copy()
+    comments_copy[""comment-id""] = comments_copy[""comment-id""].astype(str)
+
+    # Get argument to comment mapping
+    arg_comment_map = {}
+    if ""comment-id"" in relation_df.columns:
+        relation_df[""comment-id""] = relation_df[""comment-id""].astype(str)
+        arg_comment_map = dict(zip(relation_df[""arg-id""], relation_df[""comment-id""], strict=False))
+
+    # Find attribute columns in comments dataframe
+    attribute_columns = [col for col in comments.columns if col.startswith(""attribute_"")]
+    print(f""属性カラム検出: {attribute_columns}"")
+
     arguments: list[Argument] = []
     for _, row in clusters.iterrows():
         cluster_ids = [""0""]
         for cluster_column in cluster_columns:
-            cluster_ids.append(row[cluster_column])
+            cluster_ids.append(str(row[cluster_column]))  # Convert to string to ensure serializable
+
+        # Create base argument
         argument: Argument = {
-            ""arg_id"": row[""arg-id""],
-            ""argument"": row[""argument""],
-            ""x"": row[""x""],
-            ""y"": row[""y""],
+            ""arg_id"": str(row[""arg-id""]),  # Convert to string to ensure serializable
+            ""argument"": str(row[""argument""]),
+            ""x"": float(row[""x""]),  # Convert to native float
+            ""y"": float(row[""y""]),  # Convert to native float
             ""p"": 0,  # NOTE: 一旦全部0でいれる
             ""cluster_ids"": cluster_ids,
+            ""attributes"": None,
         }
+
+        # Add attributes if available
+        if attribute_columns and row[""arg-id""] in arg_comment_map:
+            comment_id = arg_comment_map[row[""arg-id""]]
+            comment_rows = comments_copy[comments_copy[""comment-id""] == comment_id]
+
+            if not comment_rows.empty:
+                comment_row = comment_rows.iloc[0]
+                attributes = {}
+                for attr_col in attribute_columns:
+                    # Remove ""attribute_"" prefix for cleaner attribute names
+                    attr_name = attr_col[len(""attribute_"") :]
+                    # Convert potential numpy types to Python native types
+                    attr_value = comment_row.get(attr_col, None)
+                    if attr_value is not None:
+                        if isinstance(attr_value, np.integer):
+                            attr_value = int(attr_value)
+                        elif isinstance(attr_value, np.floating):
+                            attr_value = float(attr_value)
+                        elif isinstance(attr_value, np.ndarray):
+                            attr_value = attr_value.tolist()
+                    attributes[attr_name] = attr_value
+
+                # Only add non-empty attributes
+                if any(v is not None for v in attributes.values()):
+                    argument[""attributes""] = attributes
+
         arguments.append(argument)
     return arguments
 
@@ -175,21 +278,41 @@ def _build_cluster_value(melted_labels: pd.DataFrame, total_num: int) -> list[Cl
             id=""0"",
             label=""全体"",
             takeaway="""",
-            value=total_num,
+            value=int(total_num),  # Convert to native int
             parent="""",
             density_rank_percentile=0,
         )
     ]
 
     for _, melted_label in melted_labels.iterrows():
+        # Convert potential NumPy types to native Python types
+        level = (
+            int(melted_label[""level""]) if isinstance(melted_label[""level""], int | np.integer) else melted_label[""level""]
+        )
+        cluster_id = str(melted_label[""id""])
+        label = str(melted_label[""label""])
+        takeaway = str(melted_label[""description""])
+        value = (
+            int(melted_label[""value""]) if isinstance(melted_label[""value""], int | np.integer) else melted_label[""value""]
+        )
+        parent = str(melted_label.get(""parent"", ""全体""))
+
+        # Handle density_rank_percentile which might be None or a numeric value
+        density_rank = melted_label.get(""density_rank_percentile"")
+        if density_rank is not None:
+            if isinstance(density_rank, float | np.floating):
+                density_rank = float(density_rank)
+            elif isinstance(density_rank, int | np.integer):
+                density_rank = int(density_rank)
+
         cluster_value = Cluster(
-            level=melted_label[""level""],
-            id=melted_label[""id""],
-            label=melted_label[""label""],
-            takeaway=melted_label[""description""],
-            value=melted_label[""value""],
-            parent=melted_label.get(""parent"", ""全体""),
-            density_rank_percentile=melted_label.get(""density_rank_percentile""),
+            level=level,
+            id=cluster_id,
+            label=label,
+            takeaway=takeaway,
+            value=value,
+            parent=parent,
+            density_rank_percentile=density_rank,
         )
         results.append(cluster_value)
     return results
@@ -217,14 +340,14 @@ def _build_comments_value(
 def _build_translations(config):
     languages = list(config.get(""translation"", {}).get(""languages"", []))
     if len(languages) > 0:
-        with open(f""outputs/{config['output_dir']}/translations.json"") as f:
+        with open(PIPELINE_DIR / f""outputs/{config['output_dir']}/translations.json"") as f:
             translations = f.read()
         return json.loads(translations)
     return {}
 
 
 def _build_property_map(
-    arguments: pd.DataFrame, hidden_properties_map: dict[str, list[str]], config: dict
+    arguments: pd.DataFrame, comments: pd.DataFrame, hidden_properties_map: dict[str, list[str]], config: dict
 ) -> dict[str, dict[str, str]]:
     property_columns = list(hidden_properties_map.keys()) + list(config[""extraction""][""categories""].keys())
     property_map = defaultdict(dict)
@@ -240,5 +363,26 @@ def _build_property_map(
     for prop in property_columns:
         for arg_id, row in arguments.iterrows():
             # LLMによるcategory classificationがうまく行かず、NaNの場合はNoneにする
-            property_map[prop][arg_id] = row[prop] if not pd.isna(row[prop]) else None
+            value = row[prop] if not pd.isna(row[prop]) else None
+
+            # Convert NumPy types to Python native types
+            if value is not None:
+                if isinstance(value, np.integer):
+                    value = int(value)
+                elif isinstance(value, np.floating):
+                    value = float(value)
+                elif isinstance(value, np.ndarray):
+                    value = value.tolist()
+                else:
+                    # Convert any other types to string to ensure serialization
+                    try:
+                        value = str(value)
+                    except Exception as e:
+                        print(f""Error converting value to string: {e}"")
+                        value = None
+
+            # Make sure arg_id is string
+            str_arg_id = str(arg_id)
+            property_map[prop][str_arg_id] = value
+
     return property_map