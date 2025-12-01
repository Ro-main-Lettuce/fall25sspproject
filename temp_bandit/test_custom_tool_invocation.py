@@ -57,12 +57,16 @@ def test_custom_tool_invocation():
     )
     
     i18n = I18N()
+    
+    mock_agent.key = ""test_agent""
+    mock_agent.role = ""test_role""
+    
     result = execute_tool_and_check_finality(
         agent_action=action,
         tools=[custom_tool],
         i18n=i18n,
-        agent_key=mock_agent.key if hasattr(mock_agent, ""key"") else None,
-        agent_role=mock_agent.role if hasattr(mock_agent, ""role"") else None,
+        agent_key=mock_agent.key,
+        agent_role=mock_agent.role,
         tools_handler=tools_handler,
         task=mock_task,
         agent=mock_agent,