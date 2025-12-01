@@ -7,14 +7,14 @@
 
 
 class AgentTools:
-    """"""Manager class for agent-related tools""""""
+    """"""Manager class for agent-related tools.""""""
 
-    def __init__(self, agents: list[BaseAgent], i18n: I18N = I18N()):
+    def __init__(self, agents: list[BaseAgent], i18n: I18N = I18N()) -> None:
         self.agents = agents
         self.i18n = i18n
 
     def tools(self) -> list[BaseTool]:
-        """"""Get all available agent tools""""""
+        """"""Get all available agent tools.""""""
         coworkers = "", "".join([f""{agent.role}"" for agent in self.agents])
 
         delegate_tool = DelegateWorkTool(