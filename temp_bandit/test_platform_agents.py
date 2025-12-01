@@ -48,7 +48,7 @@ async def test_telegram_agent_send_message(telegram_config, mock_sender):
         platform_config=telegram_config,
         llm_config=DEFAULT_TEST_CONFIG
     )
-    with patch.object(agent, 'executor_agent') as mock_executor:
+    with patch.object(agent, ""executor_agent"") as mock_executor:
         mock_executor.send_to_platform = MagicMock(return_value=(""Message sent"", ""123""))
         result = await agent.a_receive({""role"": ""user"", ""content"": ""Test message""}, mock_sender)
         assert ""Message sent"" in str(result)
@@ -61,7 +61,7 @@ async def test_telegram_agent_async_send(telegram_config, mock_sender):
         platform_config=telegram_config,
         llm_config=DEFAULT_TEST_CONFIG
     )
-    with patch.object(agent, 'executor_agent') as mock_executor:
+    with patch.object(agent, ""executor_agent"") as mock_executor:
         mock_executor.send_to_platform = MagicMock(return_value=(""Message sent"", ""123""))
         result = await agent.a_receive({""role"": ""user"", ""content"": ""Test message""}, mock_sender)
         assert ""Message sent"" in str(result)
@@ -84,7 +84,7 @@ async def test_slack_agent_send_message(slack_config, mock_sender):
         platform_config=slack_config,
         llm_config=DEFAULT_TEST_CONFIG
     )
-    with patch.object(agent, 'executor_agent') as mock_executor:
+    with patch.object(agent, ""executor_agent"") as mock_executor:
         mock_executor.send_to_platform = MagicMock(return_value=(""Message sent"", ""123""))
         result = await agent.a_receive({""role"": ""user"", ""content"": ""Test message""}, mock_sender)
         assert ""Message sent"" in str(result)
@@ -97,7 +97,7 @@ async def test_slack_agent_async_send(slack_config, mock_sender):
         platform_config=slack_config,
         llm_config=DEFAULT_TEST_CONFIG
     )
-    with patch.object(agent, 'executor_agent') as mock_executor:
+    with patch.object(agent, ""executor_agent"") as mock_executor:
         mock_executor.send_to_platform = MagicMock(return_value=(""Message sent"", ""123""))
         result = await agent.a_receive({""role"": ""user"", ""content"": ""Test message""}, mock_sender)
         assert ""Message sent"" in str(result)
@@ -120,7 +120,7 @@ async def test_discord_agent_send_message(discord_config, mock_sender):
         platform_config=discord_config,
         llm_config=DEFAULT_TEST_CONFIG
     )
-    with patch.object(agent, 'executor_agent') as mock_executor:
+    with patch.object(agent, ""executor_agent"") as mock_executor:
         mock_executor.send_to_platform = MagicMock(return_value=(""Message sent"", ""123""))
         result = await agent.a_receive({""role"": ""user"", ""content"": ""Test message""}, mock_sender)
         assert ""Message sent"" in str(result)
@@ -133,7 +133,7 @@ async def test_discord_agent_async_send(discord_config, mock_sender):
         platform_config=discord_config,
         llm_config=DEFAULT_TEST_CONFIG
     )
-    with patch.object(agent, 'executor_agent') as mock_executor:
+    with patch.object(agent, ""executor_agent"") as mock_executor:
         mock_executor.send_to_platform = MagicMock(return_value=(""Message sent"", ""123""))
         result = await agent.a_receive({""role"": ""user"", ""content"": ""Test message""}, mock_sender)
         assert ""Message sent"" in str(result)