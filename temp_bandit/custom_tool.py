@@ -1,5 +1,3 @@
-from typing import Type
-
 from crewai.tools import BaseTool
 from pydantic import BaseModel, Field
 
@@ -15,7 +13,7 @@ class MyCustomTool(BaseTool):
     description: str = (
         ""Clear description for what this tool is useful for, your agent will need this information to use it.""
     )
-    args_schema: Type[BaseModel] = MyCustomToolInput
+    args_schema: type[BaseModel] = MyCustomToolInput
 
     def _run(self, argument: str) -> str:
         # Implementation goes here