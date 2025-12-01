@@ -38,6 +38,11 @@ def generate_where_clause(df_name: str, where: Condition) -> str:
             where.value,
         )
 
+        # Always convert to string for 'in' operator to match handler behavior
+        if operator == ""in"":
+            str_values = [str(v) if v is not None else """" for v in (value or [])]
+            return f""{df_name}[{_as_literal(column_id)}].astype(str).isin({_list_of_strings(str_values)})""
+
         # Handle numeric comparisons consistently without type coercion
         if operator in [""=="", ""!="", "">"", ""<"", "">="", ""<=""]:
             # Use direct comparison operators for all numeric comparisons
@@ -59,7 +64,18 @@ def generate_where_clause(df_name: str, where: Condition) -> str:
         elif operator == ""ends_with"":
             return f""{df_name}[{_as_literal(column_id)}].str.endswith({_as_literal(value)})""  # noqa: E501
         elif operator == ""in"":
-            return f""{df_name}[{_as_literal(column_id)}].isin({_list_of_strings(value)})""  # noqa: E501
+            # Always convert string columns and string values consistently
+            has_string_values = any(isinstance(v, str) for v in (value or []))
+            str_values = [str(v) if v is not None else """" for v in (value or [])]
+            return f""""""(
+                # Convert both column and values to strings for string-like data
+                {df_name}[{_as_literal(column_id)}].astype(str).isin({_list_of_strings(str_values)})
+                if ({df_name}[{_as_literal(column_id)}].dtype.kind in ['O', 'S', 'U'] or
+                    {has_string_values})
+                else
+                # For purely numeric columns, use values directly
+                {df_name}[{_as_literal(column_id)}].isin({_list_of_strings(value or [])})
+            )""""""  # noqa: E501
         elif operator == ""is_nan"":
             return f""{df_name}[{_as_literal(column_id)}].isna()""
         elif operator == ""is_not_nan"":
@@ -69,7 +85,7 @@ def generate_where_clause(df_name: str, where: Condition) -> str:
         elif operator == ""is_false"":
             return f""{df_name}[{_as_literal(column_id)}].eq(False)""
         else:
-            raise ValueError(f""Unknown operator: {operator}"")
+            assert_never(operator)
 
     if transform.type == TransformType.COLUMN_CONVERSION:
         column_id, data_type, errors = (
@@ -198,7 +214,9 @@ def generate_where_clause_polars(where: Condition) -> str:
         elif operator == ""ends_with"":
             return f""pl.col({_as_literal(column_id)}).str.ends_with({_as_literal(value)})""  # noqa: E501
         elif operator == ""in"":
-            return f""pl.col({_as_literal(column_id)}).is_in({_list_of_strings(value)})""  # noqa: E501
+            # Convert both column and values to strings for consistent Unicode handling
+            str_values = [str(v) if v is not None else """" for v in (value or [])]
+            return f""pl.col({_as_literal(column_id)}).cast(pl.Utf8).is_in({_list_of_strings(str_values)})""  # noqa: E501
         elif operator in ["">"", "">="", ""<"", ""<=""]:
             return f""pl.col({_as_literal(column_id)}) {operator} {_as_literal(value)}""  # noqa: E501
         elif operator == ""is_nan"":