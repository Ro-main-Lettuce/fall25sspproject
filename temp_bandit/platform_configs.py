@@ -2,7 +2,7 @@
 #
 # SPDX-License-Identifier: Apache-2.0
 from abc import ABC, abstractmethod
-from pydantic import BaseModel, Field
+from pydantic import BaseModel, Field, ConfigDict
 
 
 class BaseCommsPlatformConfig(BaseModel, ABC):
@@ -17,8 +17,7 @@ def validate_config(self) -> bool:
         """"""
         pass
 
-    class Config:
-        extra = ""allow""
+    model_config = ConfigDict(extra=""allow"")
 
 
 class ReplyMonitorConfig(BaseModel):
@@ -30,5 +29,4 @@ class ReplyMonitorConfig(BaseModel):
     max_reply_messages: int = Field(default=1, gt=0)
     """"""Maximum number of messages to collect before returning.""""""
 
-    class Config:
-        extra = ""allow""
+    model_config = ConfigDict(extra=""allow"")