@@ -1,5 +1,5 @@
 import datetime
-from typing import Annotated
+from typing import Annotated, Optional
 
 from pydantic import BaseModel, ConfigDict, Field, computed_field, field_validator
 
@@ -295,3 +295,15 @@ class MessageBatchCreate(BaseModel):
     """"""Schema for batch message creation with a max of 100 messages""""""
 
     messages: list[MessageCreate] = Field(..., max_length=100)
+
+
+class SessionContextResponse(BaseModel):
+    """"""Schema for session context response with summary and messages""""""
+    
+    summary: Optional[Metamessage] = None
+    messages: list[Message]
+
+    model_config = ConfigDict(
+        from_attributes=True,
+        populate_by_name=True
+    )