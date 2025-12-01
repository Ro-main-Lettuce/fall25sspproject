@@ -1,28 +1,28 @@
 from datetime import datetime
-from typing import Any, Dict, Optional
+from typing import Any
 
 from pydantic import BaseModel, Field
 
 from crewai.utilities.serialization import to_serializable
 
 
 class BaseEvent(BaseModel):
-    """"""Base class for all events""""""
+    """"""Base class for all events.""""""
 
     timestamp: datetime = Field(default_factory=datetime.now)
     type: str
-    source_fingerprint: Optional[str] = None  # UUID string of the source entity
-    source_type: Optional[str] = None  # ""agent"", ""task"", ""crew""
-    fingerprint_metadata: Optional[Dict[str, Any]] = None  # Any relevant metadata
+    source_fingerprint: str | None = None  # UUID string of the source entity
+    source_type: str | None = None  # ""agent"", ""task"", ""crew""
+    fingerprint_metadata: dict[str, Any] | None = None  # Any relevant metadata
 
     def to_json(self, exclude: set[str] | None = None):
-        """"""
-        Converts the event to a JSON-serializable dictionary.
+        """"""Converts the event to a JSON-serializable dictionary.
 
         Args:
             exclude (set[str], optional): Set of keys to exclude from the result. Defaults to None.
 
         Returns:
             dict: A JSON-serializable dictionary.
+
         """"""
         return to_serializable(self, exclude=exclude)