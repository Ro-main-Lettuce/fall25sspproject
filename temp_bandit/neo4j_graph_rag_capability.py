@@ -4,8 +4,7 @@
 
 from typing import Any, Optional, Union
 
-from autogen import Agent, ConversableAgent, UserProxyAgent
-
+from .... import Agent, ConversableAgent, UserProxyAgent
 from .graph_query_engine import GraphStoreQueryResult
 from .graph_rag_capability import GraphRagCapability
 from .neo4j_graph_query_engine import Neo4jGraphQueryEngine