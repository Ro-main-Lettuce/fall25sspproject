@@ -357,7 +357,9 @@ def test_serialize_session_with_dict_error():
         output=CellOutput(
             channel=CellChannel.MARIMO_ERROR,
             mimetype=""text/plain"",
-            data=[{""type"": ""unknown"", ""msg"": ""Something went wrong""}],  # Dictionary instead of Error object
+            data=[
+                {""type"": ""unknown"", ""msg"": ""Something went wrong""}
+            ],  # Dictionary instead of Error object
         ),
         console=[],
         timestamp=0,