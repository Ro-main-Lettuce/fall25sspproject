@@ -75,23 +75,30 @@ def handle_filter_rows(
 
         clauses: List[pd.Series[Any]] = []
         for condition in transform.where:
-            # Get column and value without type coercion
             column = df[condition.column_id]
-            value = condition.value if condition.value is not None else """"
-
-            # Ensure string values for string operations
-            if condition.operator in [
-                ""contains"",
-                ""regex"",
-                ""starts_with"",
-                ""ends_with"",
-            ]:
-                value = str(value)
-            # Ensure list values for isin operation
+
+            # Special handling for 'in' operator
+            if condition.operator == ""in"":
+                value = condition.value
+                if value is None:
+                    value = []
+                elif not isinstance(value, (list, tuple)):
+                    value = [value]
+                # Always convert to string for consistent Unicode handling
+                str_values = [str(v) if v is not None else """" for v in value]
+                df_filter = column.astype(str).isin(str_values)
+            else:
+                value = _coerce_value(column.dtype, condition.value)
+
+            # Special handling for string operations
+            if condition.operator in [""contains"", ""regex"", ""starts_with"", ""ends_with""]:
+                if not isinstance(value, str):
+                    value = str(value) if value is not None else """"
+            # Special handling for list operations
             elif condition.operator == ""in"":
                 value = list(value) if value else []
 
-            # Handle numeric comparisons consistently without type coercion
+            # Handle numeric comparisons
             if condition.operator == ""=="":
                 df_filter = column == value
             elif condition.operator == ""!="":
@@ -114,25 +121,37 @@ def handle_filter_rows(
                 df_filter = column.isna()
             elif condition.operator == ""is_not_nan"":
                 df_filter = column.notna()
-            # Handle equality operations consistently with numeric comparisons
+            # Handle equality operations
             elif condition.operator == ""equals"":
                 df_filter = column == value
             elif condition.operator == ""does_not_equal"":
                 df_filter = column != value
             # Handle string operations
             elif condition.operator == ""contains"":
-                df_filter = column.str.contains(value, regex=False, na=False)
+                df_filter = column.str.contains(str(value), regex=False, na=False)
             elif condition.operator == ""regex"":
-                df_filter = column.str.contains(value, regex=True, na=False)
+                df_filter = column.str.contains(str(value), regex=True, na=False)
             elif condition.operator == ""starts_with"":
-                df_filter = column.str.startswith(value, na=False)
+                df_filter = column.str.startswith(str(value), na=False)
             elif condition.operator == ""ends_with"":
-                df_filter = column.str.endswith(value, na=False)
-            # Handle list operations
+                df_filter = column.str.endswith(str(value), na=False)
+            # Handle list operations with proper Unicode handling
             elif condition.operator == ""in"":
-                df_filter = column.isin(value)
+                # Always convert string columns and string values consistently
+                has_string_values = any(isinstance(v, str) for v in (value or []))
+                is_string_column = (pd.api.types.is_string_dtype(column.dtype) or
+                                  pd.api.types.is_object_dtype(column.dtype))
+
+                if has_string_values or is_string_column:
+                    # Convert both column and values to strings for string-like data
+                    str_column = column.astype(str)
+                    str_values = [str(v) if v is not None else """" for v in (value or [])]
+                    df_filter = str_column.isin(str_values)
+                else:
+                    # For purely numeric columns, use values directly
+                    df_filter = column.isin(value or [])
             else:
-                raise ValueError(f""Unknown operator: {condition.operator}"")
+                assert_never(condition.operator)
 
             clauses.append(df_filter)
 
@@ -141,7 +160,7 @@ def handle_filter_rows(
         elif transform.operation == ""remove_rows"":
             df = df[~pd.concat(clauses, axis=1).all(axis=1)]
         else:
-            raise ValueError(f""Unknown operation: {transform.operation}"")
+            assert_never(transform.operation)
 
         return df
 
@@ -163,7 +182,7 @@ def handle_group_by(
         elif transform.aggregation == ""max"":
             return group.max()
         else:
-            raise ValueError(f""Unknown aggregation: {transform.aggregation}"")
+            assert_never(transform.aggregation)
 
     @staticmethod
     def handle_aggregate(
@@ -321,7 +340,15 @@ def handle_filter_rows(
             elif condition.operator == ""ends_with"":
                 condition_expr = column.str.ends_with(value or """")
             elif condition.operator == ""in"":
-                condition_expr = column.is_in(value or [])
+                # Always convert both column and values to strings for consistent handling
+                if value is None:
+                    value = []
+                elif not isinstance(value, (list, tuple)):
+                    value = [value]
+
+                # Convert all values to strings for consistent Unicode handling
+                str_values = [str(v) if v is not None else """" for v in value]
+                condition_expr = column.cast(pl.Utf8).is_in(str_values)
             else:
                 assert_never(condition.operator)
 
@@ -372,7 +399,7 @@ def handle_group_by(
             elif agg_func == ""max"":
                 aggs.append(col(column_id).max().alias(f""{column_id}_max""))
             else:
-                raise ValueError(f""Unknown aggregation function: {agg_func}"")
+                assert_never(agg_func)
 
         return df.group_by(transform.column_ids, maintain_order=True).agg(aggs)
 
@@ -398,7 +425,7 @@ def handle_aggregate(
             elif agg_func == ""max"":
                 agg_df = selected_df.max()
             else:
-                raise ValueError(f""Unknown aggregation function: {agg_func}"")
+                assert_never(agg_func)
 
             # Rename all
             agg_df = agg_df.rename(
@@ -549,7 +576,7 @@ def handle_filter_rows(
             elif condition.operator == ""in"":
                 filter_conditions.append(column.isin(value))
             else:
-                raise ValueError(f""Unknown operator: {condition.operator}"")
+                assert_never(condition.operator)
 
         combined_condition = ibis.and_(*filter_conditions)
 
@@ -558,7 +585,7 @@ def handle_filter_rows(
         elif transform.operation == ""remove_rows"":
             return df.filter(~combined_condition)
         else:
-            raise ValueError(f""Unsupported operation: {transform.operation}"")
+            assert_never(transform.operation)
 
     @staticmethod
     def handle_group_by(
@@ -661,4 +688,43 @@ def as_sql_code(transformed_df: ""ibis.Table"") -> str | None:
             return None
 
 
-# Removed _coerce_value function as we now use direct comparisons without type coercion
+def _coerce_value(dtype: Any, value: Any) -> Any:
+    """"""Coerce value to match column dtype while preserving numeric precision.""""""
+    import numpy as np
+    import pandas as pd
+
+    # Handle None/empty values
+    if value is None:
+        return """"
+
+    # Handle string-like integers and dates
+    if hasattr(dtype, 'kind'):
+        if dtype.kind == 'O':  # Object/string type
+            try:
+                if pd.api.types.is_datetime64_any_dtype(dtype):
+                    return pd.to_datetime(value)
+                return str(value) if value is not None else """"
+            except (ValueError, TypeError):
+                return str(value) if value is not None else """"
+        elif dtype.kind == 'M':  # Datetime type
+            try:
+                return pd.to_datetime(value)
+            except (ValueError, TypeError):
+                return value
+        elif dtype.kind == 'i' and isinstance(value, float):
+            # Prevent float-to-int conversion
+            return value
+
+    # Handle numeric comparisons
+    if isinstance(value, (int, float)) and hasattr(dtype, 'kind'):
+        if dtype.kind in ('i', 'u'):  # Integer types
+            if isinstance(value, float):
+                return value  # Keep floats as-is when comparing with integers
+        elif dtype.kind == 'f':  # Float types
+            return float(value)
+
+    # Default coercion for other cases
+    try:
+        return np.array([value]).astype(dtype)[0]
+    except Exception:
+        return value