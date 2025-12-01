@@ -1,4 +1,4 @@
-from typing import Any, Dict, Optional, Union
+from typing import Any
 
 
 class LongTermMemoryItem:
@@ -8,9 +8,9 @@ def __init__(
         task: str,
         expected_output: str,
         datetime: str,
-        quality: Optional[Union[int, float]] = None,
-        metadata: Optional[Dict[str, Any]] = None,
-    ):
+        quality: float | None = None,
+        metadata: dict[str, Any] | None = None,
+    ) -> None:
         self.task = task
         self.agent = agent
         self.quality = quality