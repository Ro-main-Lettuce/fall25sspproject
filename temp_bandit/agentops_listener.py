@@ -21,15 +21,15 @@ class AgentOpsListener(BaseEventListener):
     tool_event: Optional[""agentops.ToolEvent""] = None
     session: Optional[""agentops.Session""] = None
 
-    def __init__(self):
+    def __init__(self) -> None:
         super().__init__()
 
-    def setup_listeners(self, crewai_event_bus):
+    def setup_listeners(self, crewai_event_bus) -> None:
         if not AGENTOPS_INSTALLED:
             return
 
         @crewai_event_bus.on(CrewKickoffStartedEvent)
-        def on_crew_kickoff_started(source, event: CrewKickoffStartedEvent):
+        def on_crew_kickoff_started(source, event: CrewKickoffStartedEvent) -> None:
             self.session = agentops.init()
             for agent in source.agents:
                 if self.session:
@@ -39,28 +39,28 @@ def on_crew_kickoff_started(source, event: CrewKickoffStartedEvent):
                     )
 
         @crewai_event_bus.on(CrewKickoffCompletedEvent)
-        def on_crew_kickoff_completed(source, event: CrewKickoffCompletedEvent):
+        def on_crew_kickoff_completed(source, event: CrewKickoffCompletedEvent) -> None:
             if self.session:
                 self.session.end_session(
                     end_state=""Success"",
                     end_state_reason=""Finished Execution"",
                 )
 
         @crewai_event_bus.on(ToolUsageStartedEvent)
-        def on_tool_usage_started(source, event: ToolUsageStartedEvent):
+        def on_tool_usage_started(source, event: ToolUsageStartedEvent) -> None:
             self.tool_event = agentops.ToolEvent(name=event.tool_name)
             if self.session:
                 self.session.record(self.tool_event)
 
         @crewai_event_bus.on(ToolUsageErrorEvent)
-        def on_tool_usage_error(source, event: ToolUsageErrorEvent):
+        def on_tool_usage_error(source, event: ToolUsageErrorEvent) -> None:
             agentops.ErrorEvent(exception=event.error, trigger_event=self.tool_event)
 
         @crewai_event_bus.on(TaskEvaluationEvent)
-        def on_task_evaluation(source, event: TaskEvaluationEvent):
+        def on_task_evaluation(source, event: TaskEvaluationEvent) -> None:
             if self.session:
                 self.session.create_agent(
-                    name=""Task Evaluator"", agent_id=str(source.original_agent.id)
+                    name=""Task Evaluator"", agent_id=str(source.original_agent.id),
                 )
 
 