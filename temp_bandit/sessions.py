@@ -309,6 +309,9 @@ async def get_session_context(
 ):
     """"""Get session context with latest summary and messages after that summary""""""
     try:
+        # First check if the session exists
+        await crud.get_session(db, app_id=app_id, user_id=user_id, session_id=session_id)
+        
         summary_type_enum = (
             history.SummaryType.LONG 
             if summary_type.lower() == ""long"" 