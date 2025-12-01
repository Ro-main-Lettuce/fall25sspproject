@@ -254,7 +254,7 @@ def parse_output(output: str) -> tuple[str, str, list[LLMFunction]]:
             functions.append(LLMFunction(name=func_name, description=description, scenario=scenario))
 
         if not functions:
-            raise ValueError(""Failed to parse output, expected at least one function definition"")
+            return reasoning, definitions, []
         return reasoning, definitions, functions
 
     def on_message(self: Self, context: TypespecContext, message: MessageParam) -> ""TypespecMachine"":