@@ -76,15 +76,24 @@ def save_input_file(report_input: ReportInput) -> Path:
     Returns:
         Path: 保存されたCSVファイルのパス
     """"""
-    comments = [
-        {
+    comments = []
+    for comment in report_input.comments:
+        # 基本フィールドの設定
+        comment_data = {
             ""comment-id"": comment.id,
             ""comment-body"": comment.comment,
             ""source"": comment.source,
             ""url"": comment.url,
         }
-        for comment in report_input.comments
-    ]
+
+        # 追加の属性フィールドを含める
+        for key, value in comment.dict(exclude={""id"", ""comment"", ""source"", ""url""}).items():
+            if value is not None:
+                # すでに""attribute_""プレフィックスがついているかチェック
+                comment_data[key] = value
+
+        comments.append(comment_data)
+
     input_path = settings.INPUT_DIR / f""{report_input.input}.csv""
     df = pd.DataFrame(comments)
     df.to_csv(input_path, index=False)
@@ -162,3 +171,27 @@ def launch_report_generation(report_input: ReportInput) -> None:
         set_status(report_input.input, ""error"")
         logger.error(f""Error launching report generation: {e}"")
         raise e
+
+
+def execute_aggregation(slug: str) -> bool:
+    """"""
+    broadlistenigの集約処理のみ実行する関数
+    """"""
+    try:
+        config_path = settings.CONFIG_DIR / f""{slug}.json""
+        cmd = [
+            ""python"",
+            ""hierarchical_main.py"",
+            config_path,
+            ""--skip-interaction"",
+            ""--without-html"",
+            ""-o"",
+            ""hierarchical_aggregation"",
+        ]
+        execution_dir = settings.TOOL_DIR / ""pipeline""
+        process = subprocess.Popen(cmd, cwd=execution_dir)
+        threading.Thread(target=_monitor_process, args=(process, slug), daemon=True).start()
+        return True
+    except Exception as e:
+        logger.error(f""Error executing aggregation: {e}"")
+        return False