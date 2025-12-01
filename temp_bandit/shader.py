@@ -350,7 +350,7 @@ def load_mtoon1_node_group(
             else:
                 context.blend_data.node_groups.remove(template_node_group)
 
-        # プログラムロジック的には既にremoveされている可能性もあるので、取得しなおす
+        # Logically, it may have already been removed, so retrieve it again
         old_template_node_group = context.blend_data.node_groups.get(
             backup_name(template_node_group_name, backup_suffix)
         )
@@ -413,16 +413,16 @@ def load_mtoon1_shader(
 
     backup_suffix = generate_backup_suffix()
 
-    # アペンドされるマテリアルと同名のものある場合は退避する。
-    # 将来的にはappend(do_reuse_local_id=True)で代替する。
+    # Back up if there are materials with the same name as the one being appended.
+    # In the future, this will be replaced with append(do_reuse_local_id=True).
     template_material_name = template_name(""VRM Add-on MToon 1.0"")
     old_material = context.blend_data.materials.get(template_material_name)
     if old_material:
         logger.error('Material ""%s"" already exists', template_material_name)
         old_material.name = backup_name(old_material.name, backup_suffix)
 
-    # Materialをアペンドする際にNodeTreeも同時にアペンドされる。
-    # それらと同名のNodeTreeが存在する場合は退避する。
+    # When appending a Material, NodeTree is also appended simultaneously.
+    # Back up if NodeTree with the same name exists.
     for shader_node_group_name in SHADER_NODE_GROUP_NAMES:
         name = template_name(shader_node_group_name)
         old_template_group = context.blend_data.node_groups.get(name)
@@ -472,7 +472,7 @@ def load_mtoon1_shader(
             else:
                 context.blend_data.materials.remove(template_material)
 
-        # Materialをアペンドする際に同時にアペンドされたNodeTreeを削除
+        # Remove NodeTree that was appended simultaneously when appending Material
         for shader_node_group_name in SHADER_NODE_GROUP_NAMES:
             shader_node_group_template_name = template_name(shader_node_group_name)
             template_group = context.blend_data.node_groups.get(
@@ -489,14 +489,14 @@ def load_mtoon1_shader(
                 else:
                     context.blend_data.node_groups.remove(template_group)
 
-        # プログラムロジック的には既にremoveされている可能性もあるので、取得しなおす
+        # Logically, it may have already been removed, so retrieve it again
         old_material = context.blend_data.materials.get(
             backup_name(template_material_name, backup_suffix)
         )
         if old_material:
             old_material.name = template_material_name
 
-        # 退避していたNodeTreeを復元する
+        # Restore the backed up NodeTree
         for shader_node_group_name in SHADER_NODE_GROUP_NAMES:
             name = template_name(shader_node_group_name)
             old_template_group = context.blend_data.node_groups.get(
@@ -706,7 +706,7 @@ def copy_node(
     to_node: Node,
     from_to: dict[Node, Node],
 ) -> None:
-    # ruff: noqa: SIM102  if文の可読性を高めるため、この関数内だけSIM102を無効化
+    # ruff: noqa: SIM102  Disable SIM102 only in this function to improve if statement readability
 
     from_node_color = (
         from_node.color[0],
@@ -1384,7 +1384,7 @@ def copy_node_tree_interface_socket(
     to_socket.default_attribute_name = from_socket.default_attribute_name
     to_socket.hide_value = from_socket.hide_value
     to_socket.hide_in_modifier = (
-        True  # 内部利用専用のため、モディファイアからは常に隠す
+        True  # For internal use only, always hide from modifier
     )
     to_socket.force_non_field = from_socket.force_non_field
 