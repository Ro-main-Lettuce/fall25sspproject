@@ -23,6 +23,8 @@ def __init__(
         args_schema: type[BaseModel],
         func: Callable[..., Any],
         result_as_answer: bool = False,
+        max_usage_count: int | None = None,
+        current_usage_count: int = 0,
     ) -> None:
         """"""Initialize the structured tool.
 
@@ -32,13 +34,17 @@ def __init__(
             args_schema: The pydantic model for the tool's arguments
             func: The function to run when the tool is called
             result_as_answer: Whether to return the output directly
+            max_usage_count: Maximum number of times this tool can be used. None means unlimited usage.
+            current_usage_count: Current number of times this tool has been used.
         """"""
         self.name = name
         self.description = description
         self.args_schema = args_schema
         self.func = func
         self._logger = Logger()
         self.result_as_answer = result_as_answer
+        self.max_usage_count = max_usage_count
+        self.current_usage_count = current_usage_count
 
         # Validate the function signature matches the schema
         self._validate_function_signature()