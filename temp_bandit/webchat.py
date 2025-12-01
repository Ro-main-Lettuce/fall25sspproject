@@ -57,6 +57,8 @@ def __init__(self, config: dict, ap: app.Application, logger: EventLogger):
         self.webchat_person_session = WebChatSession(id='webchatperson')
         self.webchat_group_session = WebChatSession(id='webchatgroup')
 
+        self.bot_account_id = 'webchatbot'
+
     async def send_message(
         self,
         target_type: str,
@@ -168,8 +170,15 @@ async def send_webchat_message(
                 sender=sender, message_chain=message_chain, time=datetime.now().timestamp()
             )
         else:
-            group = platform_entities.Group(id='webchatgroup', name='Group')
-            sender = platform_entities.GroupMember(id='webchatperson', nickname='User', group=group)
+            group = platform_entities.Group(
+                id='webchatgroup', name='Group', permission=platform_entities.Permission.Member
+            )
+            sender = platform_entities.GroupMember(
+                id='webchatperson',
+                member_name='User',
+                group=group,
+                permission=platform_entities.Permission.Member,
+            )
             event = platform_events.GroupMessage(
                 sender=sender, message_chain=message_chain, time=datetime.now().timestamp()
             )