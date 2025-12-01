@@ -17,7 +17,7 @@ class LLMModelInfo(pydantic.BaseModel):
 
     token_mgr: token.TokenManager
 
-    requester: requester.LLMAPIRequester
+    requester: requester.ProviderAPIRequester
 
     tool_call_supported: typing.Optional[bool] = False
 