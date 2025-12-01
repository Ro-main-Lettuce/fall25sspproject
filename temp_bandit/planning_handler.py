@@ -1,12 +1,16 @@
+import logging
 from typing import Any, List, Optional
 
 from pydantic import BaseModel, Field
 
 from crewai.agent import Agent
 from crewai.task import Task
 
+""""""Handles planning and coordination of crew tasks.""""""
+logger = logging.getLogger(__name__)
 
 class PlanPerTask(BaseModel):
+    """"""Represents a plan for a specific task.""""""
     task: str = Field(..., description=""The task for which the plan is created"")
     plan: str = Field(
         ...,
@@ -15,13 +19,15 @@ class PlanPerTask(BaseModel):
 
 
 class PlannerTaskPydanticOutput(BaseModel):
+    """"""Output format for task planning results.""""""
     list_of_plans_per_task: List[PlanPerTask] = Field(
         ...,
         description=""Step by step plan on how the agents can execute their tasks using the available tools with mastery"",
     )
 
 
 class CrewPlanner:
+    """"""Plans and coordinates the execution of crew tasks.""""""
     def __init__(self, tasks: List[Task], planning_agent_llm: Optional[Any] = None):
         self.tasks = tasks
 
@@ -68,19 +74,39 @@ def _create_planner_task(self, planning_agent: Agent, tasks_summary: str) -> Tas
             output_pydantic=PlannerTaskPydanticOutput,
         )
 
+    def _get_agent_knowledge(self, task: Task) -> List[str]:
+        """"""
+        Safely retrieve knowledge source content from the task's agent.
+
+        Args:
+            task: The task containing an agent with potential knowledge sources
+
+        Returns:
+            List[str]: A list of knowledge source strings
+        """"""
+        try:
+            if task.agent and task.agent.knowledge_sources:
+                return [source.content for source in task.agent.knowledge_sources]
+        except AttributeError:
+            logger.warning(""Error accessing agent knowledge sources"")
+        return []
+
     def _create_tasks_summary(self) -> str:
         """"""Creates a summary of all tasks.""""""
         tasks_summary = []
         for idx, task in enumerate(self.tasks):
-            tasks_summary.append(
-                f""""""
+            knowledge_list = self._get_agent_knowledge(task)
+            task_summary = f""""""
                 Task Number {idx + 1} - {task.description}
                 ""task_description"": {task.description}
                 ""task_expected_output"": {task.expected_output}
                 ""agent"": {task.agent.role if task.agent else ""None""}
                 ""agent_goal"": {task.agent.goal if task.agent else ""None""}
                 ""task_tools"": {task.tools}
-                ""agent_tools"": {task.agent.tools if task.agent else ""None""}
-                """"""
-            )
+                ""agent_tools"": %s%s"""""" % (
+                    f""[{', '.join(str(tool) for tool in task.agent.tools)}]"" if task.agent and task.agent.tools else '""agent has no tools""',
+                    f',
                ""agent_knowledge"": ""[\\""{knowledge_list[0]}\\""]""' if knowledge_list and str(knowledge_list) != ""None"" else """"
+                )
+
+            tasks_summary.append(task_summary)
         return "" "".join(tasks_summary)