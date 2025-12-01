@@ -1,27 +1,25 @@
-from typing import TYPE_CHECKING, Any, Dict, List, Optional, Sequence, Union
+from collections.abc import Sequence
+from typing import Any
 
 from crewai.agents.agent_builder.base_agent import BaseAgent
 from crewai.tools.base_tool import BaseTool
 from crewai.tools.structured_tool import CrewStructuredTool
 
 from .base_events import BaseEvent
 
-if TYPE_CHECKING:
-    from crewai.agents.agent_builder.base_agent import BaseAgent
-
 
 class AgentExecutionStartedEvent(BaseEvent):
-    """"""Event emitted when an agent starts executing a task""""""
+    """"""Event emitted when an agent starts executing a task.""""""
 
     agent: BaseAgent
     task: Any
-    tools: Optional[Sequence[Union[BaseTool, CrewStructuredTool]]]
+    tools: Sequence[BaseTool | CrewStructuredTool] | None
     task_prompt: str
     type: str = ""agent_execution_started""
 
     model_config = {""arbitrary_types_allowed"": True}
 
-    def __init__(self, **data):
+    def __init__(self, **data) -> None:
         super().__init__(**data)
         # Set fingerprint data from the agent
         if hasattr(self.agent, ""fingerprint"") and self.agent.fingerprint:
@@ -35,14 +33,14 @@ def __init__(self, **data):
 
 
 class AgentExecutionCompletedEvent(BaseEvent):
-    """"""Event emitted when an agent completes executing a task""""""
+    """"""Event emitted when an agent completes executing a task.""""""
 
     agent: BaseAgent
     task: Any
     output: str
     type: str = ""agent_execution_completed""
 
-    def __init__(self, **data):
+    def __init__(self, **data) -> None:
         super().__init__(**data)
         # Set fingerprint data from the agent
         if hasattr(self.agent, ""fingerprint"") and self.agent.fingerprint:
@@ -56,14 +54,14 @@ def __init__(self, **data):
 
 
 class AgentExecutionErrorEvent(BaseEvent):
-    """"""Event emitted when an agent encounters an error during execution""""""
+    """"""Event emitted when an agent encounters an error during execution.""""""
 
     agent: BaseAgent
     task: Any
     error: str
     type: str = ""agent_execution_error""
 
-    def __init__(self, **data):
+    def __init__(self, **data) -> None:
         super().__init__(**data)
         # Set fingerprint data from the agent
         if hasattr(self.agent, ""fingerprint"") and self.agent.fingerprint:
@@ -78,27 +76,27 @@ def __init__(self, **data):
 
 # New event classes for LiteAgent
 class LiteAgentExecutionStartedEvent(BaseEvent):
-    """"""Event emitted when a LiteAgent starts executing""""""
+    """"""Event emitted when a LiteAgent starts executing.""""""
 
-    agent_info: Dict[str, Any]
-    tools: Optional[Sequence[Union[BaseTool, CrewStructuredTool]]]
-    messages: Union[str, List[Dict[str, str]]]
+    agent_info: dict[str, Any]
+    tools: Sequence[BaseTool | CrewStructuredTool] | None
+    messages: str | list[dict[str, str]]
     type: str = ""lite_agent_execution_started""
 
     model_config = {""arbitrary_types_allowed"": True}
 
 
 class LiteAgentExecutionCompletedEvent(BaseEvent):
-    """"""Event emitted when a LiteAgent completes execution""""""
+    """"""Event emitted when a LiteAgent completes execution.""""""
 
-    agent_info: Dict[str, Any]
+    agent_info: dict[str, Any]
     output: str
     type: str = ""lite_agent_execution_completed""
 
 
 class LiteAgentExecutionErrorEvent(BaseEvent):
-    """"""Event emitted when a LiteAgent encounters an error during execution""""""
+    """"""Event emitted when a LiteAgent encounters an error during execution.""""""
 
-    agent_info: Dict[str, Any]
+    agent_info: dict[str, Any]
     error: str
     type: str = ""lite_agent_execution_error""