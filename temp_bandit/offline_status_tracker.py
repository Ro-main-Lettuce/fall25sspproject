@@ -1,14 +1,15 @@
-import logging
-import time
-import tqdm
-
-from dataclasses import dataclass, field
 import datetime
+import logging
 import platform
-import torch
+from dataclasses import dataclass, field
 
 logger = logging.getLogger(__name__)
 
+try:
+    import torch
+except ImportError:
+    pass
+
 
 @dataclass
 class System:
@@ -23,6 +24,7 @@ class System:
     pytorch_version: str = torch.__version__
 
     def __str__(self):
+        """"""String representation of the System class.""""""
         return (
             f""System: {self.system}
""
             f""Version: {self.version}
""
@@ -45,6 +47,7 @@ class OfflineStatusTracker:
     system: System = System()
 
     def __str__(self):
+        """"""String representation of the OfflineStatusTracker class.""""""
         return (
             f""Started: {self.time_started}
""
             f""Finished: {self.time_finished}
""