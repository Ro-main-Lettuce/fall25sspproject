@@ -15,10 +15,7 @@ def test_task_without_guardrail():
     agent.execute_task.return_value = ""test result""
     agent.crew = None
 
-    task = Task(
-        description=""Test task"",
-        expected_output=""Output""
-    )
+    task = Task(description=""Test task"", expected_output=""Output"")
 
     result = task.execute_sync(agent=agent)
     assert isinstance(result, TaskOutput)
@@ -27,6 +24,7 @@ def test_task_without_guardrail():
 
 def test_task_with_successful_guardrail():
     """"""Test that successful guardrail validation passes transformed result.""""""
+
     def guardrail(result: TaskOutput):
         return (True, result.raw.upper())
 
@@ -35,11 +33,7 @@ def guardrail(result: TaskOutput):
     agent.execute_task.return_value = ""test result""
     agent.crew = None
 
-    task = Task(
-        description=""Test task"",
-        expected_output=""Output"",
-        guardrail=guardrail
-    )
+    task = Task(description=""Test task"", expected_output=""Output"", guardrail=guardrail)
 
     result = task.execute_sync(agent=agent)
     assert isinstance(result, TaskOutput)
@@ -48,22 +42,20 @@ def guardrail(result: TaskOutput):
 
 def test_task_with_failing_guardrail():
     """"""Test that failing guardrail triggers retry with error context.""""""
+
     def guardrail(result: TaskOutput):
         return (False, ""Invalid format"")
 
     agent = Mock()
     agent.role = ""test_agent""
-    agent.execute_task.side_effect = [
-        ""bad result"",
-        ""good result""
-    ]
+    agent.execute_task.side_effect = [""bad result"", ""good result""]
     agent.crew = None
 
     task = Task(
         description=""Test task"",
         expected_output=""Output"",
         guardrail=guardrail,
-        max_retries=1
+        max_retries=1,
     )
 
     # First execution fails guardrail, second succeeds
@@ -77,6 +69,7 @@ def guardrail(result: TaskOutput):
 
 def test_task_with_guardrail_retries():
     """"""Test that guardrail respects max_retries configuration.""""""
+
     def guardrail(result: TaskOutput):
         return (False, ""Invalid format"")
 
@@ -89,7 +82,7 @@ def guardrail(result: TaskOutput):
         description=""Test task"",
         expected_output=""Output"",
         guardrail=guardrail,
-        max_retries=2
+        max_retries=2,
     )
 
     with pytest.raises(Exception) as exc_info:
@@ -102,6 +95,7 @@ def guardrail(result: TaskOutput):
 
 def test_guardrail_error_in_context():
     """"""Test that guardrail error is passed in context for retry.""""""
+
     def guardrail(result: TaskOutput):
         return (False, ""Expected JSON, got string"")
 
@@ -113,11 +107,12 @@ def guardrail(result: TaskOutput):
         description=""Test task"",
         expected_output=""Output"",
         guardrail=guardrail,
-        max_retries=1
+        max_retries=1,
     )
 
     # Mock execute_task to succeed on second attempt
     first_call = True
+
     def execute_task(task, context, tools):
         nonlocal first_call
         if first_call: