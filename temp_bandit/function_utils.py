@@ -134,17 +134,15 @@ def get_parameter_json_schema(k: str, v: Any, default_values: dict[str, Any]) ->
     """"""
 
     def type2description(k: str, v: Union[Annotated[type[Any], str], type[Any]]) -> str:
+        if not hasattr(v, ""__metadata__""):
+            return k
+
         # handles Annotated
-        if hasattr(v, ""__metadata__""):
-            retval = v.__metadata__[0]
-            if isinstance(retval, AG2Field):
-                return retval.description  # type: ignore[return-value]
-            else:
-                raise ValueError(
-                    f""Invalid {retval} for parameter {k}, should be a DescriptionField, got {type(retval)}""
-                )
+        retval = v.__metadata__[0]
+        if isinstance(retval, AG2Field):
+            return retval.description  # type: ignore[return-value]
         else:
-            return k
+            raise ValueError(f""Invalid {retval} for parameter {k}, should be a DescriptionField, got {type(retval)}"")
 
     schema = type2schema(v)
     if k in default_values: