@@ -60,6 +60,7 @@ def execute_tool_and_check_finality(
             task=task,
             agent=agent,
             action=agent_action,
+            original_tools=tools,  # Pass original tools to ensure custom tools work
         )
 
         # Parse tool calling