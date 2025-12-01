@@ -13,10 +13,10 @@
 """"""
 
 import time
-from dataclasses import dataclass
 from datetime import datetime
 from typing import List, Optional, Tuple
 
+from pydantic import Field
 from slack_sdk import WebClient
 from slack_sdk.errors import SlackApiError
 
@@ -37,7 +37,6 @@
 __REPLY_POLL_INTERVAL__ = 2  # Interval in seconds for polling for replies
 
 
-@dataclass
 class SlackConfig(BaseCommsPlatformConfig):
     """"""Slack-specific configuration.
 
@@ -48,17 +47,10 @@ class SlackConfig(BaseCommsPlatformConfig):
     4. Add bot to desired channel
     """"""
 
-    bot_token: str
-    """"""Bot User OAuth Token starting with xoxb-.""""""
-
-    channel_id: str
-    """"""Channel ID where messages will be sent.""""""
-
-    signing_secret: str
-    """"""Signing secret for verifying requests from Slack.""""""
-
-    app_token: Optional[str] = None
-    """"""App-level token starting with xapp- (required for Socket Mode).""""""
+    bot_token: str = Field(..., description=""Bot User OAuth Token starting with xoxb-"")
+    channel_id: str = Field(..., description=""Channel ID where messages will be sent"")
+    signing_secret: str = Field(..., description=""Signing secret for verifying requests from Slack"")
+    app_token: Optional[str] = Field(None, description=""App-level token starting with xapp- (required for Socket Mode)"")
 
     def validate_config(self) -> bool:
         if not self.bot_token or not self.bot_token.startswith(""xoxb-""):
@@ -69,6 +61,9 @@ def validate_config(self) -> bool:
             raise ValueError(""signing_secret is required"")
         return True
 
+    class Config:
+        extra = ""allow""
+
 
 class SlackHandler:
     """"""Handles Slack client operations with synchronous functionality.""""""