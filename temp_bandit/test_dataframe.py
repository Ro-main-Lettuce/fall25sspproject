@@ -277,8 +277,6 @@ def test_polars_groupby_alias() -> None:
         """"""Test that group by operations use original column names correctly.""""""
         import polars as pl
 
-        import marimo as mo
-
         # Create a test dataframe with age and group columns
         df = pl.DataFrame(
             {