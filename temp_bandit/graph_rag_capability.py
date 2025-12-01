@@ -4,9 +4,8 @@
 #
 # Portions derived from https://github.com/microsoft/autogen are under the MIT License.
 # SPDX-License-Identifier: MIT
-from autogen.agentchat.contrib.capabilities.agent_capability import AgentCapability
-from autogen.agentchat.conversable_agent import ConversableAgent
-
+from ...conversable_agent import ConversableAgent
+from ..capabilities.agent_capability import AgentCapability
 from .graph_query_engine import GraphQueryEngine
 
 