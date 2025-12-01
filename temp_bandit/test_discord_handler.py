@@ -2,7 +2,7 @@
 from unittest.mock import MagicMock, AsyncMock
 import discord
 import asyncio
-import threading
+
 from typing import Dict, List, Optional, Union, Tuple
 
 from autogen.agentchat.contrib.comms.discord_agent import DiscordHandler
@@ -40,9 +40,7 @@ async def test_discord_handler_start(discord_handler):
 
 @pytest.mark.asyncio
 async def test_discord_handler_start_auth_error(discord_handler):
-    discord_handler._client.login = AsyncMock(
-        side_effect=discord.LoginFailure()
-    )
+    discord_handler._client.login = AsyncMock(side_effect=discord.LoginFailure())
     with pytest.raises(PlatformAuthenticationError):
         await discord_handler.start()
 
@@ -62,37 +60,28 @@ async def test_discord_handler_send_long_message(discord_handler):
     mock_message1 = MagicMock(id=123)
     mock_message2 = MagicMock(id=124)
     
-    discord_handler._channel.send = AsyncMock(
-        side_effect=[mock_message1, mock_message2]
-    )
+    discord_handler._channel.send = AsyncMock(side_effect=[mock_message1, mock_message2])
     
     result = await discord_handler.send_message(long_message)
     assert result[0] == ""Message sent successfully""
     assert discord_handler._channel.send.call_count == 2
 
 @pytest.mark.asyncio
 async def test_discord_handler_send_message_rate_limit(discord_handler):
-    discord_handler._channel.send = AsyncMock(
-        side_effect=discord.RateLimited(5.0)
-    )
+    discord_handler._channel.send = AsyncMock(side_effect=discord.RateLimited(5.0))
     with pytest.raises(PlatformRateLimitError) as exc_info:
         await discord_handler.send_message(""Test message"")
     assert exc_info.value.retry_after == 5
 
 @pytest.mark.asyncio
 async def test_discord_handler_send_message_connection_error(discord_handler):
-    discord_handler._channel.send = AsyncMock(
-        side_effect=discord.ConnectionClosed()
-    )
+    discord_handler._channel.send = AsyncMock(side_effect=discord.ConnectionClosed())
     with pytest.raises(PlatformConnectionError):
         await discord_handler.send_message(""Test message"")
 
 @pytest.mark.asyncio
 async def test_discord_handler_wait_for_replies(discord_handler):
-    discord_handler._message_replies[""123""] = [
-        {""content"": ""Reply 1"", ""author"": ""User1"", ""timestamp"": ""2023-01-01T12:00:00""},
-        {""content"": ""Reply 2"", ""author"": ""User2"", ""timestamp"": ""2023-01-01T12:00:01""}
-    ]
+    discord_handler._message_replies[""123""] = [{""content"": ""Reply 1"", ""author"": ""User1"", ""timestamp"": ""2023-01-01T12:00:00""}, {""content"": ""Reply 2"", ""author"": ""User2"", ""timestamp"": ""2023-01-01T12:00:01""}]
     replies = await discord_handler.wait_for_replies(""123"", timeout_minutes=1)
     assert len(replies) == 2
     assert replies[0][""content""] == ""Reply 1""