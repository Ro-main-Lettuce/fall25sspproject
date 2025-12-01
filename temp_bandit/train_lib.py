@@ -147,7 +147,7 @@ def create_name_map(
     name_map[name] = i
 
   # Bake in name groups from nametags.py
-  for first, *rest in nametags.name_groups:
+  for first, *rest in nametags.NAME_GROUPS:
     if first not in name_map:
       continue
     for name in rest: