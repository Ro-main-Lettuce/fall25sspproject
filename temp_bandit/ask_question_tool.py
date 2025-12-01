@@ -1,4 +1,3 @@
-from typing import Optional
 
 from pydantic import BaseModel, Field
 
@@ -12,7 +11,7 @@ class AskQuestionToolSchema(BaseModel):
 
 
 class AskQuestionTool(BaseAgentTool):
-    """"""Tool for asking questions to coworkers""""""
+    """"""Tool for asking questions to coworkers.""""""
 
     name: str = ""Ask question to coworker""
     args_schema: type[BaseModel] = AskQuestionToolSchema
@@ -21,7 +20,7 @@ def _run(
         self,
         question: str,
         context: str,
-        coworker: Optional[str] = None,
+        coworker: str | None = None,
         **kwargs,
     ) -> str:
         coworker = self._get_coworker(coworker, **kwargs)