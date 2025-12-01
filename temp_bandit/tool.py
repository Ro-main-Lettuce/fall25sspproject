@@ -89,6 +89,21 @@ def register_for_execution(self, agent: ""ConversableAgent"") -> None:
         """"""
         agent.register_for_execution()(self)
 
+    def register_tool(self, agent: ""ConversableAgent"") -> None:
+        """"""
+        Register a tool to be both proposed and executed by an agent.
+
+        Equivalent to calling both `register_for_llm` and `register_for_execution` with the same agent.
+
+        Note: This will not make the agent recommend and execute the call in the one step. If the agent
+        recommends the tool, it will need to be the next agent to speak in order to execute the tool.
+
+        Args:
+            agent (ConversableAgent): The agent to which the tool will be registered.
+        """"""
+        self.register_for_llm(agent)
+        self.register_for_execution(agent)
+
     def __call__(self, *args: Any, **kwargs: Any) -> Any:
         """"""Execute the tool by calling its underlying function with the provided arguments.
 