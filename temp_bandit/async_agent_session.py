@@ -24,7 +24,7 @@
 logger = logging.getLogger(__name__)
 
 
-// DEPRECATED: use agent/trpc_agent/agent_session.py instead!
+# DEPRECATED: use agent/trpc_agent/agent_session.py instead!
 class AsyncAgentSession(AgentInterface):
     def __init__(self, application_id: str | None= None, trace_id: str | None = None, settings: Optional[Dict[str, Any]] = None):
         """"""Initialize a new agent session""""""