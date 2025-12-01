@@ -24,21 +24,9 @@ def script_path(script_name):
 def main():
     parser = argparse.ArgumentParser(description=""クラスタ評価一括実行スクリプト"")
     parser.add_argument(""dataset"", help=""データセットID（例: 2）"")
-    parser.add_argument(
-        ""--level"",
-        choices=[""1"", ""2"", ""both""],
-        default=""both"",
-        help=""評価レベル（1, 2, both）"",
-    )
-    parser.add_argument(
-        ""--max-samples"", type=int, help=""LLMプロンプトに含める最大意見数（省略可）""
-    )
-    parser.add_argument(
-        ""--mode"",
-        choices=[""api"", ""print""],
-        default=""api"",
-        help=""LLM評価の実行モード（api or print）"",
-    )
+    parser.add_argument(""--level"", choices=[""1"", ""2"", ""both""], default=""both"", help=""評価レベル（1, 2, both）"")
+    parser.add_argument(""--max-samples"", type=int, help=""LLMプロンプトに含める最大意見数（省略可）"")
+    parser.add_argument(""--mode"", choices=[""api"", ""print""], default=""api"", help=""LLM評価の実行モード（api or print）"")
     parser.add_argument(""--model"", help=""使用するOpenAIモデル名（例: gpt-4o）"")
     args = parser.parse_args()
 
@@ -67,19 +55,15 @@ def main():
 
             run_command(cmd, f""LLMプロンプト出力（level {level}）"")
 
-            print(
-                f""📄 定性評価用プロンプトを output/{dataset}/prompt_level{level}.txt に保存しました。""
-            )
-            print(
-                f""💾 実行結果を output/{dataset}/evaluation_consistency_llm_level{level}.json に保存すれば、CSVやHTMLで利用できます。""
-            )
+            print(f""📄 定性評価用プロンプトを output/{dataset}/prompt_level{level}.txt に保存しました。"")
+            print(f""💾 実行結果を output/{dataset}/evaluation_consistency_llm_level{level}.json に保存すれば、CSVやHTMLで利用できます。"")
         return
 
     for level in levels:
         print(f""
=== ステップ1: シルエットスコア（level {level}） ==="")
         required_files = [
             input_dir / f""silhouette_umap_level{level}_clusters.json"",
-            input_dir / f""silhouette_umap_level{level}_points.json"",
+            input_dir / f""silhouette_umap_level{level}_points.json""
         ]
         if all_exist(required_files):
             for f in required_files:
@@ -105,16 +89,14 @@ def main():
 
             run_command(cmd, f""LLM評価（level {level}）"")
 
-    print(""
=== ステップ3: CSV出力 ==="")
+    print(f""
=== ステップ3: CSV出力 ==="")
     run_command(f""python {script_path('generate_csv.py')} {dataset}"", ""CSV出力"")
-    print(""✓ CSV出力完了:"")
+    print(f""✓ CSV出力完了:"")
     print(f"" - クラスタ: {output_dir / 'cluster_evaluation.csv'}"")
     print(f"" - 意見:     {output_dir / 'comment_evaluation.csv'}"")
 
-    print(""
=== ステップ4: HTMLレポート生成 ==="")
-    run_command(
-        f""python {script_path('generate_html.py')} {dataset}"", ""HTMLレポート生成""
-    )
+    print(f""
=== ステップ4: HTMLレポート生成 ==="")
+    run_command(f""python {script_path('generate_html.py')} {dataset}"", ""HTMLレポート生成"")
     print(f""✓ HTML出力完了: {output_dir / 'report.html'}"")
 
 