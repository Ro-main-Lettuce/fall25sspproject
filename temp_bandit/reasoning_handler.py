@@ -81,7 +81,7 @@ def __create_initial_plan(self) -> Tuple[str, bool]:
             system_prompt = self.i18n.retrieve(""reasoning"", ""initial_plan"").format(
                 role=self.agent.role,
                 goal=self.agent.goal,
-                backstory=self.agent.backstory
+                backstory=self.__get_agent_backstory()
             )
             
             response = self.llm.call(
@@ -116,7 +116,7 @@ def __refine_plan_if_needed(self, plan: str, ready: bool) -> Tuple[str, bool]:
                 system_prompt = self.i18n.retrieve(""reasoning"", ""refine_plan"").format(
                     role=self.agent.role,
                     goal=self.agent.goal,
-                    backstory=self.agent.backstory
+                    backstory=self.__get_agent_backstory()
                 )
                 
                 response = self.llm.call(
@@ -173,7 +173,7 @@ def __call_with_function(self, prompt: str, prompt_type: str) -> Tuple[str, bool
             system_prompt = self.i18n.retrieve(""reasoning"", prompt_type).format(
                 role=self.agent.role,
                 goal=self.agent.goal,
-                backstory=self.agent.backstory
+                backstory=self.__get_agent_backstory()
             )
             
             response = self.llm.call(
@@ -203,7 +203,7 @@ def __call_with_function(self, prompt: str, prompt_type: str) -> Tuple[str, bool
                 system_prompt = self.i18n.retrieve(""reasoning"", prompt_type).format(
                     role=self.agent.role,
                     goal=self.agent.goal,
-                    backstory=self.agent.backstory
+                    backstory=self.__get_agent_backstory()
                 )
                 
                 fallback_response = self.llm.call(
@@ -219,6 +219,15 @@ def __call_with_function(self, prompt: str, prompt_type: str) -> Tuple[str, bool
                 self.logger.error(f""Error during fallback text parsing: {str(inner_e)}"")
                 return ""Failed to generate a plan due to an error."", True  # Default to ready to avoid getting stuck
 
+    def __get_agent_backstory(self) -> str:
+        """"""
+        Safely gets the agent's backstory, providing a default if not available.
+        
+        Returns:
+            str: The agent's backstory or a default value.
+        """"""
+        return getattr(self.agent, ""backstory"", ""No backstory provided"")
+
     def __create_reasoning_prompt(self) -> str:
         """"""
         Creates a prompt for the agent to reason about the task.
@@ -231,6 +240,7 @@ def __create_reasoning_prompt(self) -> str:
         return self.i18n.retrieve(""reasoning"", ""create_plan_prompt"").format(
             role=self.agent.role,
             goal=self.agent.goal,
+            backstory=self.__get_agent_backstory(),
             description=self.task.description,
             expected_output=self.task.expected_output,
             tools=available_tools
@@ -261,6 +271,7 @@ def __create_refine_prompt(self, current_plan: str) -> str:
         return self.i18n.retrieve(""reasoning"", ""refine_plan_prompt"").format(
             role=self.agent.role,
             goal=self.agent.goal,
+            backstory=self.__get_agent_backstory(),
             current_plan=current_plan
         )
 