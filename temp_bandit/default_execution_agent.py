@@ -34,6 +34,9 @@
 from portia.execution_agents.utils.step_summarizer import StepSummarizer
 from portia.execution_context import get_execution_context
 from portia.model import GenerativeModel, Message
+
+if TYPE_CHECKING:
+    from portia.portia import ExecutionHooks
 from portia.tool import ToolRunContext
 
 if TYPE_CHECKING:
@@ -610,6 +613,7 @@ def __init__(  # noqa: PLR0913
         agent_memory: AgentMemory,
         end_user: EndUser,
         tool: Tool | None = None,
+        execution_hooks: ExecutionHooks | None = None,
     ) -> None:
         """"""Initialize the agent.
 
@@ -620,11 +624,14 @@ def __init__(  # noqa: PLR0913
             agent_memory (AgentMemory): The agent memory to be used for the task.
             end_user (EndUser): The end user for this execution
             tool (Tool | None): The tool to be used for the task (optional).
+            execution_hooks (ExecutionHooks | None): Hooks that can be used to modify or add
+                extra functionality.
 
         """"""
         super().__init__(step, plan_run, config, end_user, agent_memory, tool)
         self.verified_args: VerifiedToolInputs | None = None
         self.new_clarifications: list[Clarification] = []
+        self.execution_hooks = execution_hooks
 
     def clarifications_or_continue(
         self,
@@ -706,6 +713,10 @@ def execute_sync(self) -> Output:
             clarifications=self.plan_run.get_clarifications_for_step(),
         )
 
+        execution_hooks = getattr(self, ""execution_hooks"", None)
+        if execution_hooks and execution_hooks.before_tool_call:
+            execution_hooks.before_tool_call(tool_run_ctx, self.tool)
+
         model = self.config.get_execution_model()
 
         tools = [
@@ -778,8 +789,14 @@ def execute_sync(self) -> Output:
 
         app = graph.compile()
         invocation_result = app.invoke({""messages"": [], ""step_inputs"": []})
-        return process_output(
+        result = process_output(
             invocation_result[""messages""],
             self.tool,
             self.new_clarifications,
         )
+
+        execution_hooks = getattr(self, ""execution_hooks"", None)
+        if execution_hooks and execution_hooks.after_tool_call:
+            execution_hooks.after_tool_call(tool_run_ctx, self.tool, result)
+
+        return result