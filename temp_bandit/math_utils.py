@@ -6,7 +6,7 @@
 # SPDX-License-Identifier: MIT
 from typing import Optional
 
-from autogen import DEFAULT_MODEL, oai
+from . import DEFAULT_MODEL, oai
 
 _MATH_PROMPT = ""{problem} Solve the problem carefully. Simplify your answer as much as possible. Put the final answer in \\boxed{{}}.""
 _MATH_CONFIG = {