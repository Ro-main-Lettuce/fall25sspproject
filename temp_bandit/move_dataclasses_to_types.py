@@ -8,7 +8,7 @@
 def run(codebase: Codebase):
     # Only process files in src/codegen
     src_codegen_prefix = ""src/codegen""
-    
+
     # Special cases that should not be moved
     special_cases = [
         ""src/codegen/sdk/core/dataclasses/usage.py""  # UsageType and UsageKind are widely used