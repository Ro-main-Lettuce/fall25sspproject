@@ -1,11 +1,10 @@
-from codegen.cli.utils.types import DecoratedFunction
 import ast
-import dataclasses
 import importlib
 import importlib.util
-from dataclasses import dataclass
 from pathlib import Path
 
+from codegen.cli.utils.types import DecoratedFunction
+
 
 class CodegenFunctionVisitor(ast.NodeVisitor):
     def __init__(self):