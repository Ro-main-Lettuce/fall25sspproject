@@ -14,7 +14,7 @@
 from ...tools import entities as tools_entities
 
 
-class ModelScopeChatCompletions(requester.LLMAPIRequester):
+class ModelScopeChatCompletions(requester.ProviderAPIRequester):
     """"""ModelScope ChatCompletion API 请求器""""""
 
     client: openai.AsyncClient