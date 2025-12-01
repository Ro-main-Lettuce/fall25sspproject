@@ -1,11 +1,8 @@
-from typing import TYPE_CHECKING, Any
+from typing import Any
 
 from crewai.agents.agent_builder.base_agent import BaseAgent
 from crewai.utilities.events.base_events import BaseEvent
 
-if TYPE_CHECKING:
-    from crewai.agents.agent_builder.base_agent import BaseAgent
-
 
 class KnowledgeRetrievalStartedEvent(BaseEvent):
     """"""Event emitted when a knowledge retrieval is started.""""""