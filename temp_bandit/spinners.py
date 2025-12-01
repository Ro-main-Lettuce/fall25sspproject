@@ -1,10 +1,9 @@
 """"""Consistent spinner styles for the CLI.""""""
 
-from codegen.cli.rich.types import SpinnerConfig
-from dataclasses import dataclass
-
 from rich.status import Status
 
+from codegen.cli.rich.types import SpinnerConfig
+
 
 def create_spinner(text: str) -> Status:
     """"""Create a spinner with consistent styling.