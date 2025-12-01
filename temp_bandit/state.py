@@ -51,6 +51,8 @@ def sidebar_index(self) -> int:
             elif ""hosting"" in route:
                 return 0
             elif ""api-reference"" in route:
+                return 2
+            elif ""enterprise"" in route:
                 return 3
             else:
                 return 0