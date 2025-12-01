@@ -5,7 +5,7 @@ def __init__(
         type: str,
         description: str,
         relationships: str,
-    ):
+    ) -> None:
         self.name = name
         self.type = type
         self.description = description