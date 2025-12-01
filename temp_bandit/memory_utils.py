@@ -1,9 +1,9 @@
-from codegen.shared.performance.types import MemoryStats
 import os
-from dataclasses import dataclass
 
 import psutil
 
+from codegen.shared.performance.types import MemoryStats
+
 
 def get_memory_stats() -> MemoryStats:
     process = psutil.Process(os.getpid())