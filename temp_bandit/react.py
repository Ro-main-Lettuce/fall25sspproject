@@ -6,6 +6,7 @@
 from app.agent.base import BaseAgent
 from app.llm import LLM
 from app.schema import AgentState, Memory
+from app.agent.toolcall import ToolCallAgent
 
 
 class ReActAgent(BaseAgent, ABC):
@@ -36,3 +37,17 @@ async def step(self) -> str:
         if not should_act:
             return ""Thinking complete - no action needed""
         return await self.act()
+
+
+class ReactAgent(ToolCallAgent):
+    """"""
+    A React agent that can use tools.
+    
+    This class extends ToolCallAgent to provide tool handling capabilities
+    while maintaining compatibility with code that expects a ReactAgent.
+    """"""
+    
+    name: str = ""react""
+    description: str = ""an agent that implements the ReAct paradigm with tool handling capabilities.""
+    
+    # Inherit system_prompt, next_step_prompt, and other attributes from ToolCallAgent