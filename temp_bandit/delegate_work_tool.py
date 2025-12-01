@@ -14,7 +14,12 @@ class DelegateWorkToolSchema(BaseModel):
 
 
 class DelegateWorkTool(BaseAgentTool):
-    """"""Tool for delegating work to coworkers""""""
+    """"""Tool for delegating work to other agents in the crew.
+    
+    Attributes:
+        result_as_answer (bool): When True, returns the delegated agent's result
+            as the final answer instead of metadata about delegation.
+    """"""
 
     name: str = ""Delegate work to coworker""
     args_schema: type[BaseModel] = DelegateWorkToolSchema