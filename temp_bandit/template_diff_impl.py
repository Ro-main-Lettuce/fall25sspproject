@@ -6,12 +6,10 @@
 import os
 import json
 import tempfile
-import logging
-from typing import Dict, Any, List, Optional, Tuple
+from typing import Dict, Any, Optional, Tuple
 
 from api.agent_server.interface import AgentInterface
 from api.agent_server.models import AgentSseEvent, AgentMessage, AgentStatus, MessageKind
-from api.config import CONFIG
 
 from log import get_logger
 
@@ -310,9 +308,9 @@ def _generate_unified_diff(self, server_files: Dict[str, str], frontend_files: D
         
         for filename, content in server_files.items():
             diff_lines.append(f""diff --git a/server/{filename} b/server/{filename}"")
-            diff_lines.append(f""new file mode 100644"")
+            diff_lines.append(""new file mode 100644"")
             diff_lines.append(f""index 0000000..{hash(content) & 0xFFFFFF:x}"")
-            diff_lines.append(f""--- /dev/null"")
+            diff_lines.append(""--- /dev/null"")
             diff_lines.append(f""+++ b/server/{filename}"")
             diff_lines.append(f""@@ -0,0 +1,{content.count(chr(10)) + 1} @@"")
             
@@ -321,9 +319,9 @@ def _generate_unified_diff(self, server_files: Dict[str, str], frontend_files: D
         
         for filename, content in frontend_files.items():
             diff_lines.append(f""diff --git a/frontend/{filename} b/frontend/{filename}"")
-            diff_lines.append(f""new file mode 100644"")
+            diff_lines.append(""new file mode 100644"")
             diff_lines.append(f""index 0000000..{hash(content) & 0xFFFFFF:x}"")
-            diff_lines.append(f""--- /dev/null"")
+            diff_lines.append(""--- /dev/null"")
             diff_lines.append(f""+++ b/frontend/{filename}"")
             diff_lines.append(f""@@ -0,0 +1,{content.count(chr(10)) + 1} @@"")
             