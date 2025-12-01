@@ -1,21 +1,23 @@
-from typing import Any, Callable, Optional, Union
+from collections.abc import Callable
+from typing import Any
 
 from crewai.utilities.events.base_events import BaseEvent
 
 
 class LLMGuardrailStartedEvent(BaseEvent):
-    """"""Event emitted when a guardrail task starts
+    """"""Event emitted when a guardrail task starts.
 
     Attributes:
         guardrail: The guardrail callable or LLMGuardrail instance
         retry_count: The number of times the guardrail has been retried
+
     """"""
 
     type: str = ""llm_guardrail_started""
-    guardrail: Union[str, Callable]
+    guardrail: str | Callable
     retry_count: int
 
-    def __init__(self, **data):
+    def __init__(self, **data) -> None:
         from inspect import getsource
 
         from crewai.tasks.llm_guardrail import LLMGuardrail
@@ -29,10 +31,10 @@ def __init__(self, **data):
 
 
 class LLMGuardrailCompletedEvent(BaseEvent):
-    """"""Event emitted when a guardrail task completes""""""
+    """"""Event emitted when a guardrail task completes.""""""
 
     type: str = ""llm_guardrail_completed""
     success: bool
     result: Any
-    error: Optional[str] = None
+    error: str | None = None
     retry_count: int