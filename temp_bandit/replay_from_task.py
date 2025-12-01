@@ -4,11 +4,11 @@
 
 
 def replay_task_command(task_id: str) -> None:
-    """"""
-    Replay the crew execution from a specific task.
+    """"""Replay the crew execution from a specific task.
 
     Args:
       task_id (str): The ID of the task to replay from.
+
     """"""
     command = [""uv"", ""run"", ""replay"", task_id]
 