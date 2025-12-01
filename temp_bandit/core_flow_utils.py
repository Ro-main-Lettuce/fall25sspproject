@@ -17,7 +17,7 @@
 from pydantic import BaseModel
 
 
-def get_possible_return_constants(function: callable) -> Optional[List[str]]:
+def get_possible_return_constants(function: Callable[..., Any]) -> Optional[List[str]]:
     """"""Extract possible string return values from a function by analyzing its source code.
     
     Analyzes the function's source code using AST to identify string constants that