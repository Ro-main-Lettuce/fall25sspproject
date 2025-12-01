@@ -1,17 +1,17 @@
-from typing import Any, Optional
+from typing import Any
 
 from crewai.tasks.task_output import TaskOutput
 from crewai.utilities.events.base_events import BaseEvent
 
 
 class TaskStartedEvent(BaseEvent):
-    """"""Event emitted when a task starts""""""
+    """"""Event emitted when a task starts.""""""
 
     type: str = ""task_started""
-    context: Optional[str]
-    task: Optional[Any] = None
+    context: str | None
+    task: Any | None = None
 
-    def __init__(self, **data):
+    def __init__(self, **data) -> None:
         super().__init__(**data)
         # Set fingerprint data from the task
         if hasattr(self.task, ""fingerprint"") and self.task.fingerprint:
@@ -25,13 +25,13 @@ def __init__(self, **data):
 
 
 class TaskCompletedEvent(BaseEvent):
-    """"""Event emitted when a task completes""""""
+    """"""Event emitted when a task completes.""""""
 
     output: TaskOutput
     type: str = ""task_completed""
-    task: Optional[Any] = None
+    task: Any | None = None
 
-    def __init__(self, **data):
+    def __init__(self, **data) -> None:
         super().__init__(**data)
         # Set fingerprint data from the task
         if hasattr(self.task, ""fingerprint"") and self.task.fingerprint:
@@ -45,13 +45,13 @@ def __init__(self, **data):
 
 
 class TaskFailedEvent(BaseEvent):
-    """"""Event emitted when a task fails""""""
+    """"""Event emitted when a task fails.""""""
 
     error: str
     type: str = ""task_failed""
-    task: Optional[Any] = None
+    task: Any | None = None
 
-    def __init__(self, **data):
+    def __init__(self, **data) -> None:
         super().__init__(**data)
         # Set fingerprint data from the task
         if hasattr(self.task, ""fingerprint"") and self.task.fingerprint:
@@ -65,13 +65,13 @@ def __init__(self, **data):
 
 
 class TaskEvaluationEvent(BaseEvent):
-    """"""Event emitted when a task evaluation is completed""""""
+    """"""Event emitted when a task evaluation is completed.""""""
 
     type: str = ""task_evaluation""
     evaluation_type: str
-    task: Optional[Any] = None
+    task: Any | None = None
 
-    def __init__(self, **data):
+    def __init__(self, **data) -> None:
         super().__init__(**data)
         # Set fingerprint data from the task
         if hasattr(self.task, ""fingerprint"") and self.task.fingerprint: