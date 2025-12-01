@@ -1,16 +1,28 @@
 """"""Test that context=[] is respected and doesn't include previous task outputs.""""""
-import pytest
 from unittest import mock
 
+import pytest
+
 from crewai import Agent, Crew, Process, Task
 from crewai.tasks.task_output import OutputFormat, TaskOutput
 from crewai.utilities.formatter import (
     aggregate_raw_outputs_from_task_outputs,
     aggregate_raw_outputs_from_tasks,
 )
 
+
 def test_context_empty_list():
-    """"""Test that context=[] is respected and doesn't include previous task outputs.""""""
+    """"""Test that context=[] is respected and doesn't include previous task outputs.
+    
+    This test verifies that when a task has context=[], the _get_context method
+    correctly uses task_outputs instead of an empty context list.
+    
+    Returns:
+        None
+        
+    Raises:
+        AssertionError: If the context handling doesn't work as expected
+    """"""
     
     
     researcher = Agent(