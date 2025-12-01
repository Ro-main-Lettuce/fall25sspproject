@@ -63,8 +63,7 @@ def validate_config(self) -> bool:
             raise ValueError(""destination_id is required"")
         return True
 
-    class Config:
-        extra = ""allow""
+    model_config = ConfigDict(extra=""allow"")
 
 
 class TelegramHandler: