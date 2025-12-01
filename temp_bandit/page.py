@@ -37,7 +37,7 @@ def more_posts(current_post: dict) -> rx.Component:
 
     for path, document in selected_posts:
         meta = document.metadata
-        posts.append(card_content(meta=meta, path=path.replace(""blog/"", """")))
+        posts.append(card_content(meta=meta, path=f""/blog/{path}""))
     return rx.el.section(
         rx.el.h2(
             ""More Posts"",