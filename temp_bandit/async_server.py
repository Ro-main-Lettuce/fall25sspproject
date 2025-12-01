@@ -36,6 +36,7 @@
 from api.agent_server.interface import AgentInterface
 from trpc_agent.agent_session import TrpcAgentSession
 from nicegui_agent.agent_session import NiceguiAgentSession
+from laravel_agent.agent_session import LaravelAgentSession
 from api.agent_server.template_diff_impl import TemplateDiffAgentImplementation
 from api.config import CONFIG
 
@@ -285,6 +286,7 @@ async def message(
             ""template_diff"": TemplateDiffAgentImplementation,
             ""trpc_agent"": TrpcAgentSession,
             ""nicegui_agent"": NiceguiAgentSession,
+            ""laravel_agent"": LaravelAgentSession,
         }
 
         if template_id not in agent_types: