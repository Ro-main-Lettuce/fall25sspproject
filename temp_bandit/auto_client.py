@@ -586,6 +586,8 @@ def from_provider(
                     ""anthropic"" in model_name.lower() or ""claude"" in model_name.lower()
                 ):
                     default_mode = instructor.Mode.BEDROCK_TOOLS
+                elif model_name and ""mistral"" in model_name.lower():
+                    default_mode = instructor.Mode.BEDROCK_MISTRAL_JSON
                 else:
                     default_mode = instructor.Mode.BEDROCK_JSON
             else: