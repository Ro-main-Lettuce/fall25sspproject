@@ -1,13 +1,13 @@
-from typing import Any, Dict, Optional
+from typing import Any
 
 
 class ShortTermMemoryItem:
     def __init__(
         self,
         data: Any,
-        agent: Optional[str] = None,
-        metadata: Optional[Dict[str, Any]] = None,
-    ):
+        agent: str | None = None,
+        metadata: dict[str, Any] | None = None,
+    ) -> None:
         self.data = data
         self.agent = agent
         self.metadata = metadata if metadata is not None else {}