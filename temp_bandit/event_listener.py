@@ -120,6 +120,7 @@ def on_crew_completed(source, event: CrewKickoffCompletedEvent):
                 ""completed"",
                 final_string_output,
             )
+            self.formatter.stop_live()
 
         @crewai_event_bus.on(CrewKickoffFailedEvent)
         def on_crew_failed(source, event: CrewKickoffFailedEvent):
@@ -262,6 +263,7 @@ def on_flow_finished(source, event: FlowFinishedEvent):
             self.formatter.update_flow_status(
                 self.formatter.current_flow_tree, event.flow_name, source.flow_id
             )
+            self.formatter.stop_live()
 
         @crewai_event_bus.on(MethodExecutionStartedEvent)
         def on_method_execution_started(source, event: MethodExecutionStartedEvent):