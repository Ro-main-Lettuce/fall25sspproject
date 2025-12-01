@@ -6,17 +6,21 @@
 be more successful than the OneShotAgent.
 """"""
 
-from __future__ import annotations  # noqa: I001
+from __future__ import annotations
 
 from typing import TYPE_CHECKING, Any
 
 from langchain_core.messages import SystemMessage
+
+if TYPE_CHECKING:
+    from portia.portia import ExecutionHooks
 from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
 from langgraph.graph import END, START, MessagesState, StateGraph
 from langgraph.prebuilt import ToolNode
 
 from portia.errors import InvalidAgentError
 from portia.execution_agents.base_execution_agent import BaseExecutionAgent
+from portia.execution_agents.context import StepInput  # noqa: TC001
 from portia.execution_agents.execution_utils import (
     AgentNode,
     next_state_after_tool_call,
@@ -27,8 +31,6 @@
 from portia.execution_agents.utils.step_summarizer import StepSummarizer
 from portia.execution_context import get_execution_context
 from portia.tool import ToolRunContext
-from portia.execution_agents.context import StepInput  # noqa: TC001
-
 
 if TYPE_CHECKING:
     from langchain.tools import StructuredTool
@@ -168,6 +170,7 @@ def __init__(  # noqa: PLR0913
         agent_memory: AgentMemory,
         end_user: EndUser,
         tool: Tool | None = None,
+        execution_hooks: ExecutionHooks | None = None,
     ) -> None:
         """"""Initialize the OneShotAgent.
 
@@ -178,9 +181,12 @@ def __init__(  # noqa: PLR0913
             agent_memory (AgentMemory): The agent memory for persisting outputs.
             end_user (EndUser): The end user for the execution.
             tool (Tool | None): The tool to be used for the task (optional).
+            execution_hooks (ExecutionHooks | None): Hooks that can be used to modify or add
+                extra functionality.
 
         """"""
         super().__init__(step, plan_run, config, end_user, agent_memory, tool)
+        self.execution_hooks = execution_hooks
 
     def execute_sync(self) -> Output:
         """"""Run the core execution logic of the task.
@@ -202,6 +208,10 @@ def execute_sync(self) -> Output:
             clarifications=self.plan_run.get_clarifications_for_step(),
         )
 
+        execution_hooks = getattr(self, ""execution_hooks"", None)
+        if execution_hooks and execution_hooks.before_tool_call:
+            execution_hooks.before_tool_call(tool_run_ctx, self.tool)
+
         model = self.config.get_execution_model()
         tools = [
             self.tool.to_langchain_with_artifact(
@@ -240,4 +250,10 @@ def execute_sync(self) -> Output:
         app = graph.compile()
         invocation_result = app.invoke({""messages"": [], ""step_inputs"": []})
 
-        return process_output(invocation_result[""messages""], self.tool)
+        result = process_output(invocation_result[""messages""], self.tool)
+
+        execution_hooks = getattr(self, ""execution_hooks"", None)
+        if execution_hooks and execution_hooks.after_tool_call:
+            execution_hooks.after_tool_call(tool_run_ctx, self.tool, result)
+
+        return result