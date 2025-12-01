@@ -182,7 +182,7 @@ async def verify_chatgpt_api_key(api_key: str = Depends(verify_admin_api_key)) -
 
         _ = request_to_chat_openai(
             messages=test_messages,
-            model=""gpt-3.5-turbo"" if not use_azure else None,
+            model=""gpt-4o-mini"" if not use_azure else None,
             max_tokens=1,
         )
 