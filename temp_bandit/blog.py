@@ -165,6 +165,7 @@ def blogs():
             title=document.metadata[""title""],
             description=document.metadata[""description""],
             image=document.metadata[""image""],
+            url=f""https://reflex.dev{route}"",
         ),
     )(lambda doc=document: page(doc, route))
 