@@ -673,9 +673,9 @@ def test_apply_formatting_with_none_values(self) -> None:
             ""integers"": lambda x: -100 if x is None else x * 2,
             ""floats"": lambda x: ""---"" if x is None else f""{x:.1f}"",
             ""booleans"": lambda x: ""MISSING"" if x is None else str(x).upper(),
-            ""dates"": lambda x: ""No Date""
-            if x is None
-            else x.strftime(""%Y-%m-%d""),
+            ""dates"": lambda x: (
+                ""No Date"" if x is None else x.strftime(""%Y-%m-%d"")
+            ),
             ""lists"": lambda x: ""Empty"" if x is None else f""List({len(x)})"",
         }
 
@@ -822,6 +822,65 @@ def test_get_sample_values_with_metadata_only_frame(df: Any) -> None:
     assert sample_values == []
 
 
+@pytest.mark.skipif(not HAS_DEPS, reason=""optional dependencies not installed"")
+def test_get_sample_values_returns_primitives() -> None:
+    """"""Test that get_sample_values always returns primitive types.""""""
+    import polars as pl
+
+    def is_primitive(value: Any) -> bool:
+        return isinstance(
+            value,
+            (
+                str,
+                int,
+                float,
+                bool,
+                type(None),
+                datetime.datetime,
+                datetime.date,
+            ),
+        )
+
+    class Enum:
+        A = ""a""
+        B = ""b""
+        C = ""c""
+
+    # Create a DataFrame with various types including categorical/enum-like columns
+    df = pl.DataFrame(
+        {
+            ""category"": pl.Series([""A"", ""B"", ""C""], dtype=pl.Categorical),
+            ""mixed"": pl.Series([""str"", ""123"", ""45.67""]),
+            ""list"": pl.Series([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
+            ""dict"": pl.Series(
+                [
+                    {""a"": 1, ""b"": Enum.A},
+                    {""c"": 3, ""d"": Enum.B},
+                    {""e"": 5, ""f"": Enum.C},
+                ]
+            ),
+            ""enum"": pl.Series([Enum.A, Enum.B, Enum.C]),
+            ""dates"": [
+                datetime.datetime(2021, 1, 1),
+                datetime.datetime(2021, 1, 2),
+                datetime.datetime(2021, 1, 3),
+            ],
+        },
+    )
+
+    manager: NarwhalsTableManager[Any] = NarwhalsTableManager.from_dataframe(
+        df
+    )
+
+    # Verify all values are primitives
+    for column in df.columns:
+        values = manager.get_sample_values(column)
+        for val in values:
+            assert is_primitive(val), (
+                f""Column {column} returned non-primitive or non-datetime value: {val} of type {type(val)}""
+            )
+
+
 @pytest.mark.skipif(not HAS_DEPS, reason=""optional dependencies not installed"")
 @pytest.mark.parametrize(
     ""df"",