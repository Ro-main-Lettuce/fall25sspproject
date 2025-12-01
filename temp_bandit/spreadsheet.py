@@ -109,6 +109,13 @@ async def get_spreadsheet_data(file_name: str, api_key: str = Depends(verify_adm
             if ""url"" in df.columns:
                 comment[""url""] = row.get(""url"")
 
+            # その他のカラムを属性として追加
+            for col in df.columns:
+                if col not in [""comment-id"", ""comment"", ""source"", ""url""] and not pd.isna(row.get(col)):
+                    # attribute_プレフィックスをつける
+                    attribute_key = f""attribute_{col}"" if not col.startswith(""attribute_"") else col
+                    comment[attribute_key] = str(row.get(col))
+
             comments.append(comment)
 
         return {""status"": ""success"", ""file_name"": file_name, ""comments"": comments, ""total"": len(comments)}