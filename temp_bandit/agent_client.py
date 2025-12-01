@@ -112,7 +112,7 @@ async def continue_conversation(self,
             if role == ""user"":
                 msg = UserMessage(role=role, content=content)
             else:
-                msg = AgentMessage(role=""assistant"", content=content, agentState=None, unifiedDiff=None, kind=MessageKind.STAGE_RESULT)
+                msg = AgentMessage(role=""assistant"", content=content, agentState=None, unifiedDiff=None, kind=MessageKind.STAGE_RESULT, app_name=None, commit_message=None)
 
             messages_history_casted.append(msg)
 