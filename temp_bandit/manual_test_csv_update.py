@@ -5,10 +5,10 @@
 """"""
 
 import os
+import sys
+import tempfile
 import time
 from pathlib import Path
-import tempfile
-import sys
 
 from crewai.knowledge.knowledge import Knowledge
 from crewai.knowledge.source.csv_knowledge_source import CSVKnowledgeSource