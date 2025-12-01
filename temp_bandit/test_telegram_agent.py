@@ -31,7 +31,7 @@
 
 @pytest.mark.asyncio
 async def test_telegram_config_validation():
-    config = TelegramConfig(bot_token=""123456:ABC-DEF"", destination_id=""@testchannel"")
+    config = TelegramConfig(bot_token=""test-token"", destination_id=""test-channel"")
     assert config.validate_config() is True
 
     with pytest.raises(ValueError, match=""bot_token is required""):