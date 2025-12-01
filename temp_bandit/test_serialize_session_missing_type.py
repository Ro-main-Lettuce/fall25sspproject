@@ -13,7 +13,9 @@ def test_serialize_session_with_dict_error_missing_type():
         output=CellOutput(
             channel=CellChannel.MARIMO_ERROR,
             mimetype=""text/plain"",
-            data=[{""msg"": ""Something went wrong""}],  # Dictionary with missing type key
+            data=[
+                {""msg"": ""Something went wrong""}
+            ],  # Dictionary with missing type key
         ),
         console=[],
         timestamp=0,