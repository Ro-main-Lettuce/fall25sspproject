@@ -5,7 +5,7 @@
 
 
 class PlatformError(Exception):
-    """"""Base exception for all platform-related errors.""""""
+    """"""Base exception for all communication platform-related errors.""""""
 
     def __init__(
         self,
@@ -59,34 +59,3 @@ class PlatformMessageError(PlatformError):
     def __init__(self, message: str, message_id: Optional[str] = None, **kwargs):
         self.message_id = message_id
         super().__init__(message, **kwargs)
-
-
-# MS - MOVE THESE TO THEIR RESPECTIVE CLASSES
-
-
-# Slack-specific errors
-class SlackWorkspaceError(PlatformError):
-    """"""Raised when there's an error with Slack workspace operations.""""""
-
-    pass
-
-
-# Teams-specific errors
-class TeamsChannelError(PlatformError):
-    """"""Raised when there's an error with Teams channels.""""""
-
-    pass
-
-
-# WhatsApp-specific errors
-class WhatsAppTemplateError(PlatformError):
-    """"""Raised when there's an error with WhatsApp message templates.""""""
-
-    pass
-
-
-# Telegram-specific errors
-class TelegramBotError(PlatformError):
-    """"""Raised when there's an error with Telegram bot operations.""""""
-
-    pass