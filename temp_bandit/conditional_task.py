@@ -1,4 +1,5 @@
-from typing import Any, Callable
+from collections.abc import Callable
+from typing import Any
 
 from pydantic import Field
 
@@ -8,8 +9,7 @@
 
 
 class ConditionalTask(Task):
-    """"""
-    A task that can be conditionally executed based on the output of another task.
+    """"""A task that can be conditionally executed based on the output of another task.
     Note: This cannot be the only task you have in your crew and cannot be the first since its needs context from the previous task.
     """"""
 
@@ -22,19 +22,19 @@ def __init__(
         self,
         condition: Callable[[Any], bool],
         **kwargs,
-    ):
+    ) -> None:
         super().__init__(**kwargs)
         self.condition = condition
 
     def should_execute(self, context: TaskOutput) -> bool:
-        """"""
-        Determines whether the conditional task should be executed based on the provided context.
+        """"""Determines whether the conditional task should be executed based on the provided context.
 
         Args:
             context (Any): The context or output from the previous task that will be evaluated by the condition.
 
         Returns:
             bool: True if the task should be executed, False otherwise.
+
         """"""
         return self.condition(context)
 