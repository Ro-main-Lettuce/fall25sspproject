@@ -1,4 +1,4 @@
-from typing import Type, Union, get_args, get_origin
+from typing import Dict, List, Type, Union, get_args, get_origin
 
 from pydantic import BaseModel
 
@@ -10,40 +10,83 @@ def get_schema(self) -> str:
         """"""
         Public method to get the schema of a Pydantic model.
 
-        :param model: The Pydantic model class to generate schema for.
         :return: String representation of the model schema.
         """"""
-        return self._get_model_schema(self.model)
-
-    def _get_model_schema(self, model, depth=0) -> str:
-        indent = ""    "" * depth
-        lines = [f""{indent}{{""]
-        for field_name, field in model.model_fields.items():
-            field_type_str = self._get_field_type(field, depth + 1)
-            lines.append(f""{indent}    {field_name}: {field_type_str},"")
-        lines[-1] = lines[-1].rstrip("","")  # Remove trailing comma from last item
-        lines.append(f""{indent}}}"")
-        return ""
"".join(lines)
-
-    def _get_field_type(self, field, depth) -> str:
+        return ""{
"" + self._get_model_schema(self.model) + ""
}""
+
+    def _get_model_schema(self, model: Type[BaseModel], depth: int = 0) -> str:
+        indent = "" "" * 4 * depth
+        lines = [
+            f""{indent}    {field_name}: {self._get_field_type(field, depth + 1)}""
+            for field_name, field in model.model_fields.items()
+        ]
+        return "",
"".join(lines)
+
+    def _get_field_type(self, field, depth: int) -> str:
         field_type = field.annotation
-        if get_origin(field_type) is list:
+        origin = get_origin(field_type)
+
+        if origin in {list, List}:
             list_item_type = get_args(field_type)[0]
-            if isinstance(list_item_type, type) and issubclass(
-                list_item_type, BaseModel
-            ):
-                nested_schema = self._get_model_schema(list_item_type, depth + 1)
-                return f""List[
{nested_schema}
{' ' * 4 * depth}]""
-            else:
-                return f""List[{list_item_type.__name__}]""
-        elif get_origin(field_type) is Union:
-            union_args = get_args(field_type)
-            if type(None) in union_args:
-                non_none_type = next(arg for arg in union_args if arg is not type(None))
-                return f""Optional[{self._get_field_type(field.__class__(annotation=non_none_type), depth)}]""
+            return self._format_list_type(list_item_type, depth)
+
+        if origin in {dict, Dict}:
+            key_type, value_type = get_args(field_type)
+            return f""Dict[{key_type.__name__}, {value_type.__name__}]""
+
+        if origin is Union:
+            return self._format_union_type(field_type, depth)
+
+        if isinstance(field_type, type) and issubclass(field_type, BaseModel):
+            nested_schema = self._get_model_schema(field_type, depth)
+            nested_indent = "" "" * 4 * depth
+            return f""{field_type.__name__}
{nested_indent}{{
{nested_schema}
{nested_indent}}}""
+
+        return field_type.__name__
+
+    def _format_list_type(self, list_item_type, depth: int) -> str:
+        if isinstance(list_item_type, type) and issubclass(list_item_type, BaseModel):
+            nested_schema = self._get_model_schema(list_item_type, depth + 1)
+            nested_indent = "" "" * 4 * (depth)
+            return f""List[
{nested_indent}{{
{nested_schema}
{nested_indent}}}
{nested_indent}]""
+        return f""List[{list_item_type.__name__}]""
+
+    def _format_union_type(self, field_type, depth: int) -> str:
+        args = get_args(field_type)
+        if type(None) in args:
+            # It's an Optional type
+            non_none_args = [arg for arg in args if arg is not type(None)]
+            if len(non_none_args) == 1:
+                inner_type = self._get_field_type_for_annotation(
+                    non_none_args[0], depth
+                )
+                return f""Optional[{inner_type}]""
             else:
-                return f""Union[{', '.join(arg.__name__ for arg in union_args)}]""
-        elif isinstance(field_type, type) and issubclass(field_type, BaseModel):
-            return self._get_model_schema(field_type, depth)
+                # Union with None and multiple other types
+                inner_types = "", "".join(
+                    self._get_field_type_for_annotation(arg, depth)
+                    for arg in non_none_args
+                )
+                return f""Optional[Union[{inner_types}]]""
         else:
-            return getattr(field_type, ""__name__"", str(field_type))
+            # General Union type
+            inner_types = "", "".join(
+                self._get_field_type_for_annotation(arg, depth) for arg in args
+            )
+            return f""Union[{inner_types}]""
+
+    def _get_field_type_for_annotation(self, annotation, depth: int) -> str:
+        origin = get_origin(annotation)
+        if origin in {list, List}:
+            list_item_type = get_args(annotation)[0]
+            return self._format_list_type(list_item_type, depth)
+        if origin in {dict, Dict}:
+            key_type, value_type = get_args(annotation)
+            return f""Dict[{key_type.__name__}, {value_type.__name__}]""
+        if origin is Union:
+            return self._format_union_type(annotation, depth)
+        if isinstance(annotation, type) and issubclass(annotation, BaseModel):
+            nested_schema = self._get_model_schema(annotation, depth)
+            nested_indent = "" "" * 4 * depth
+            return f""{annotation.__name__}
{nested_indent}{{
{nested_schema}
{nested_indent}}}""
+        return annotation.__name__