@@ -63,8 +63,7 @@ def validate_config(self) -> bool:
             raise ValueError(""bot_token, guild_name, and channel_name are required"")
         return True
 
-    class Config:
-        extra = ""allow""
+    model_config = ConfigDict(extra=""allow"")
 
 
 class DiscordHandler: