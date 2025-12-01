@@ -410,7 +410,7 @@ def main():
                     func_args_str = func_call.arguments
 
                     messages.append(
-                        {
+                        {  # type: ignore
                             ""role"": ""assistant"",
                             ""tool_calls"": [
                                 {