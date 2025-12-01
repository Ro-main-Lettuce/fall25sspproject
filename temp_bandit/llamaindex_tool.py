@@ -1,9 +1,8 @@
 from typing import Any, Optional, Type, cast
 
+from crewai.tools import BaseTool
 from pydantic import BaseModel, Field
 
-from crewai_tools.tools.base_tool import BaseTool
-
 
 class LlamaIndexTool(BaseTool):
     """"""Tool to wrap LlamaIndex tools/query engines.""""""
@@ -19,6 +18,10 @@ def _run(
         from llama_index.core.tools import BaseTool as LlamaBaseTool
 
         tool = cast(LlamaBaseTool, self.llama_index_tool)
+
+        if self.result_as_answer:
+            return tool(*args, **kwargs).content
+
         return tool(*args, **kwargs)
 
     @classmethod