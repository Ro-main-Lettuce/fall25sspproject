@@ -1,9 +1,21 @@
 import json
 import os
+import sys
 import traceback
 from datetime import datetime, timedelta
 from pathlib import Path
 
+# serverディレクトリをパスに追加
+current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
+if current_dir not in sys.path:
+    sys.path.insert(0, current_dir)
+
+try:
+    from src.services.llm_pricing import LLMPricing
+except ImportError:
+    print(""Warning: Could not import LLMPricing"")
+    LLMPricing = None
+
 PIPELINE_DIR = Path(__file__).parent
 
 with open(PIPELINE_DIR / ""hierarchical_specs.json"") as f:
@@ -250,22 +262,10 @@ def run_step(step, func, config):
     token_usage_output = config.get(""token_usage_output"", 0)
 
     if provider and model and token_usage_input > 0 and token_usage_output > 0:
-        import os
-        import sys
-
-        current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
-
-        # current_dirはserverディレクトリを指す
-        if current_dir not in sys.path:
-            sys.path.insert(0, current_dir)
-
-        try:
-            from src.services.llm_pricing import LLMPricing
-
+        if LLMPricing:
             estimated_cost = LLMPricing.calculate_cost(provider, model, token_usage_input, token_usage_output)
             print(f""Estimated cost: ${estimated_cost:.4f} ({provider} {model})"")
-        except ImportError as e:
-            print(f""Warning: Could not import LLMPricing: {e}"")
+        else:
             estimated_cost = 0.0
 
     # update status after running...