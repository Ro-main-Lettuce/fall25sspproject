@@ -34,7 +34,7 @@ def __init__(self, ts_node: TSNode, file_node_id: NodeId, ctx: CodebaseContext,
         super().__init__(ts_node, file_node_id, ctx, parent)
         open_tag = self.ts_node.child_by_field_name(""open_tag"") or self.ts_node
         name_node = open_tag.child_by_field_name(""name"")
-        self._name_node = self._parse_expression(name_node, default=Name)
+        self._name_node = self._parse_expression(name_node, default=Name) if name_node else None
         self.children  # Force parse children of this JSX element
 
     @cached_property
@@ -95,7 +95,8 @@ def props(self) -> list[JSXProp]:
         Returns:
             list[JSXProp]: A list of JSXProp objects representing each attribute on the element.
         """"""
-        return [self._parse_expression(x.ts_node, default=JSXProp) for x in self._attribute_nodes]
+        # Cast the result to list[JSXProp] to satisfy type checking
+        return [self._parse_expression(x.ts_node, default=JSXProp) for x in self._attribute_nodes]  # type: ignore
 
     @reader
     def get_prop(self, name: str) -> JSXProp | None:
@@ -124,7 +125,8 @@ def attributes(self) -> list[JSXProp]:
         Returns:
             list[JSXProp]: A list of JSXProp objects representing each attribute/prop on the JSXElement.
         """"""
-        return [self._parse_expression(x.ts_node, default=JSXProp) for x in self._attribute_nodes]
+        # Cast the result to list[JSXProp] to satisfy type checking
+        return [self._parse_expression(x.ts_node, default=JSXProp) for x in self._attribute_nodes]  # type: ignore
 
     @writer
     def set_name(self, name: str) -> None:
@@ -140,11 +142,18 @@ def set_name(self, name: str) -> None:
         """"""
         # This should correctly set the name of both the opening and closing tags
         if open_tag := self.ts_node.child_by_field_name(""open_tag""):
-            name_node = self._parse_expression(open_tag.child_by_field_name(""name""), default=Name)
-            name_node.edit(name)
+            open_name_node = open_tag.child_by_field_name(""name"")
+            if open_name_node:
+                name_node = self._parse_expression(open_name_node, default=Name)
+                if name_node:
+                    name_node.edit(name)
+
             if close_tag := self.ts_node.child_by_field_name(""close_tag""):
-                name_node = self._parse_expression(close_tag.child_by_field_name(""name""), default=Name)
-                name_node.edit(name)
+                close_name_node = close_tag.child_by_field_name(""name"")
+                if close_name_node:
+                    name_node = self._parse_expression(close_name_node, default=Name)
+                    if name_node:
+                        name_node.edit(name)
         else:
             # If the element is self-closing, we only need to edit the name of the element
             super().set_name(name)
@@ -168,8 +177,11 @@ def add_prop(self, prop_name: str, prop_value: str) -> None:
             last_prop = self.props[-1]
             # Extra padding is handled by the insert_after method on prop
             last_prop.insert_after(f""{prop_name}={prop_value}"", newline=False)
-        else:
+        elif self._name_node is not None:
             self._name_node.insert_after(f"" {prop_name}={prop_value}"", newline=False)
+        else:
+            msg = ""Cannot add prop: element has no name node""
+            raise ValueError(msg)
 
     @property
     @reader