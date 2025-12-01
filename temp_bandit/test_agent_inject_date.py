@@ -10,26 +10,29 @@ def test_agent_inject_date():
     
     Tests that when inject_date=True, the current date is added to the task description.
     """"""
-    agent = Agent(
-        role=""test_agent"",
-        goal=""test_goal"",
-        backstory=""test_backstory"",
-        inject_date=True,
-    )
-    
-    task = Task(
-        description=""Test task"",
-        expected_output=""Test output"",
-        agent=agent,
-    )
-    
-    with patch.object(Agent, 'execute_task', return_value=""Task executed"") as mock_execute:
-        agent.execute_task(task)
+    with patch('datetime.datetime') as mock_datetime:
+        mock_datetime.now.return_value = datetime(2025, 1, 1)
+        
+        agent = Agent(
+            role=""test_agent"",
+            goal=""test_goal"",
+            backstory=""test_backstory"",
+            inject_date=True,
+        )
         
-        called_task = mock_execute.call_args[0][0]
+        task = Task(
+            description=""Test task"",
+            expected_output=""Test output"",
+            agent=agent,
+        )
         
-        current_date = datetime.now().strftime(""%Y-%m-%d"")
-        assert f""Current Date: {current_date}"" in called_task.description
+        # Store original description
+        original_description = task.description
+        
+        agent._inject_date_to_task(task)
+        
+        assert ""Current Date: 2025-01-01"" in task.description
+        assert task.description != original_description
 
 
 def test_agent_without_inject_date():
@@ -41,6 +44,7 @@ def test_agent_without_inject_date():
         role=""test_agent"",
         goal=""test_goal"",
         backstory=""test_backstory"",
+        # inject_date is False by default
     )
     
     task = Task(
@@ -51,41 +55,40 @@ def test_agent_without_inject_date():
     
     original_description = task.description
     
-    with patch.object(Agent, 'execute_task', return_value=""Task executed"") as mock_execute:
-        agent.execute_task(task)
-        
-        called_task = mock_execute.call_args[0][0]
-        
-        assert ""Current Date:"" not in called_task.description
-        assert called_task.description == original_description
+    agent._inject_date_to_task(task)
+    
+    assert task.description == original_description
 
 
 def test_agent_inject_date_custom_format():
     """"""Test that the inject_date flag with custom date_format works correctly.
     
     Tests that when inject_date=True with a custom date_format, the date is formatted correctly.
     """"""
-    agent = Agent(
-        role=""test_agent"",
-        goal=""test_goal"",
-        backstory=""test_backstory"",
-        inject_date=True,
-        date_format=""%d/%m/%Y"",
-    )
-    
-    task = Task(
-        description=""Test task"",
-        expected_output=""Test output"",
-        agent=agent,
-    )
-    
-    with patch.object(Agent, 'execute_task', return_value=""Task executed"") as mock_execute:
-        agent.execute_task(task)
+    with patch('datetime.datetime') as mock_datetime:
+        mock_datetime.now.return_value = datetime(2025, 1, 1)
+        
+        agent = Agent(
+            role=""test_agent"",
+            goal=""test_goal"",
+            backstory=""test_backstory"",
+            inject_date=True,
+            date_format=""%d/%m/%Y"",
+        )
+        
+        task = Task(
+            description=""Test task"",
+            expected_output=""Test output"",
+            agent=agent,
+        )
+        
+        # Store original description
+        original_description = task.description
         
-        called_task = mock_execute.call_args[0][0]
+        agent._inject_date_to_task(task)
         
-        current_date = datetime.now().strftime(""%d/%m/%Y"")
-        assert f""Current Date: {current_date}"" in called_task.description
+        assert ""Current Date: 01/01/2025"" in task.description
+        assert task.description != original_description
 
 
 def test_agent_inject_date_invalid_format():
@@ -109,6 +112,6 @@ def test_agent_inject_date_invalid_format():
     
     original_description = task.description
     
-    agent.execute_task(task)
+    agent._inject_date_to_task(task)
     
     assert task.description == original_description