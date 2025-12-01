@@ -1269,7 +1269,7 @@ def call_script(
     Returns:
         EventSpec: An event that will execute the client side javascript.
     """"""
-    callback_kwargs = {}
+    callback_kwargs = {""callback"": None}
     if callback is not None:
         callback_kwargs = {
             ""callback"": str(