@@ -4,8 +4,7 @@
 
 from typing import Any, Optional, Union
 
-from autogen import Agent, ConversableAgent, UserProxyAgent
-
+from .... import Agent, ConversableAgent, UserProxyAgent
 from .falkor_graph_query_engine import FalkorGraphQueryEngine
 from .graph_query_engine import GraphStoreQueryResult
 from .graph_rag_capability import GraphRagCapability