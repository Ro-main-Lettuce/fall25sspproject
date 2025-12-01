@@ -23,7 +23,7 @@
 
 import time
 from importlib.metadata import version
-from typing import TYPE_CHECKING
+from typing import TYPE_CHECKING, Any, Callable
 
 from portia.clarification import (
     Clarification,
@@ -92,9 +92,37 @@ class ExecutionHooks:
     that arise during the run of a plan.
     """"""
 
-    def __init__(self, clarification_handler: ClarificationHandler | None = None) -> None:
-        """"""Initialize ExecutionHooks with default values.""""""
+    def __init__(
+        self,
+        clarification_handler: ClarificationHandler | None = None,
+        before_first_execution_step: Callable[[Plan, PlanRun], None] | None = None,
+        before_execution_step: Callable[[Plan, PlanRun, Step, int], None] | None = None,
+        after_execution_step: Callable[
+            [Plan, PlanRun, Step, int, Output | None], None
+        ] | None = None,
+        after_last_execution_step: Callable[[Plan, PlanRun, Output | None], None] | None = None,
+        before_tool_call: Callable[[ToolRunContext, Tool | None], None] | None = None,
+        after_tool_call: Callable[[ToolRunContext, Tool | None, Any], None] | None = None,
+    ) -> None:
+        """"""Initialize ExecutionHooks with default values.
+
+        Args:
+            clarification_handler: A handler for clarifications that arise during the run of a plan.
+            before_first_execution_step: Called before the first step of a plan run is executed.
+            before_execution_step: Called before each step of a plan run is executed.
+            after_execution_step: Called after each step of a plan run is executed.
+            after_last_execution_step: Called after the last step of a plan run is executed.
+            before_tool_call: Called before a tool call is made.
+            after_tool_call: Called after a tool call is made.
+
+        """"""
         self.clarification_handler = clarification_handler
+        self.before_first_execution_step = before_first_execution_step
+        self.before_execution_step = before_execution_step
+        self.after_execution_step = after_execution_step
+        self.after_last_execution_step = after_last_execution_step
+        self.before_tool_call = before_tool_call
+        self.after_tool_call = after_tool_call
 
 
 class Portia:
@@ -587,10 +615,16 @@ def _execute_plan_run(self, plan: Plan, plan_run: PlanRun) -> PlanRun:
 
         last_executed_step_output = self._get_last_executed_step_output(plan, plan_run)
         introspection_agent = self._get_introspection_agent()
+
+        if self.execution_hooks and self.execution_hooks.before_first_execution_step:
+            self.execution_hooks.before_first_execution_step(plan, plan_run)
         for index in range(plan_run.current_step_index, len(plan.steps)):
             step = plan.steps[index]
             plan_run.current_step_index = index
 
+            if self.execution_hooks and self.execution_hooks.before_execution_step:
+                self.execution_hooks.before_execution_step(plan, plan_run, step, index)
+
             # Handle the introspection outcome
             (plan_run, pre_step_outcome) = self._handle_introspection_outcome(
                 introspection_agent=introspection_agent,
@@ -645,6 +679,11 @@ def _execute_plan_run(self, plan: Plan, plan_run: PlanRun) -> PlanRun:
                     f""Step output - {last_executed_step_output.get_summary()!s}"",
                 )
 
+                if self.execution_hooks and self.execution_hooks.after_execution_step:
+                    self.execution_hooks.after_execution_step(
+                        plan, plan_run, step, index, last_executed_step_output
+                    )
+
             if self._raise_clarifications(plan_run, last_executed_step_output, plan):
                 return plan_run
 
@@ -654,6 +693,11 @@ def _execute_plan_run(self, plan: Plan, plan_run: PlanRun) -> PlanRun:
                 f""New PlanRun State: {plan_run.model_dump_json(indent=4)}"",
             )
 
+        if self.execution_hooks and self.execution_hooks.after_last_execution_step:
+            self.execution_hooks.after_last_execution_step(
+                plan, plan_run, last_executed_step_output
+            )
+
         if last_executed_step_output:
             plan_run.outputs.final_output = self._get_final_output(
                 plan,
@@ -890,6 +934,7 @@ def _get_agent_for_step(
             self.storage,
             self.initialize_end_user(plan_run.end_user_id),
             tool,
+            execution_hooks=self.execution_hooks,
         )
 
     def _log_replan_with_portia_cloud_tools(