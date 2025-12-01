@@ -1,8 +1,8 @@
-from typing import Any, Dict, Optional
+from typing import Any
 
 
 class UserMemoryItem:
-    def __init__(self, data: Any, user: str, metadata: Optional[Dict[str, Any]] = None):
+    def __init__(self, data: Any, user: str, metadata: dict[str, Any] | None = None) -> None:
         self.data = data
         self.user = user
         self.metadata = metadata if metadata is not None else {}