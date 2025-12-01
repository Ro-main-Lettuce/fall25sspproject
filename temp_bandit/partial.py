@@ -79,6 +79,8 @@ def _process_generic_arg(
         )
         # Special handling for Union types (types.UnionType isn't subscriptable)
         if arg_origin in UNION_ORIGINS:
+            if arg_origin is types.UnionType and sys.version_info >= (3, 10):
+                return Union.__getitem__(modified_nested_args)  # type: ignore
             return Union[modified_nested_args]  # type: ignore
 
         return arg_origin[modified_nested_args]
@@ -466,9 +468,12 @@ def _wrap_models(field: FieldInfo) -> tuple[object, FieldInfo]:
                 modified_args = tuple(_process_generic_arg(arg) for arg in generic_args)
 
                 # Reconstruct the generic type with modified arguments
-                tmp_field.annotation = (
-                    generic_base[modified_args] if generic_base else None
-                )
+                if generic_base in UNION_ORIGINS and generic_base is types.UnionType and sys.version_info >= (3, 10):
+                    tmp_field.annotation = Union.__getitem__(modified_args)  # type: ignore
+                else:
+                    tmp_field.annotation = (
+                        generic_base[modified_args] if generic_base else None
+                    )
             # If the field is a BaseModel, then recursively convert it's
             # attributes to optionals.
             elif isinstance(annotation, type) and issubclass(annotation, BaseModel):