@@ -4,9 +4,6 @@
 This implementation provides a simple agent that returns basic diff output
 without complex generation logic, useful for testing the template system.
 """"""
-import os
-import tempfile
-import shutil
 import dagger
 from typing import Dict, Any, Optional
 from anyio.streams.memory import MemoryObjectSendStream