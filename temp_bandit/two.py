@@ -1,7 +1,9 @@
-from bespokelabs.curator import LLM
-from datasets import Dataset
-import logging
 import argparse
+import logging
+
+from datasets import Dataset
+
+from bespokelabs.curator import LLM
 
 logger = logging.getLogger(""bespokelabs.curator"")
 logger.setLevel(logging.INFO)