@@ -10,7 +10,7 @@
 from ...tools import entities as tools_entities
 
 
-class GeminiChatCompletions(requester.LLMAPIRequester):
+class GeminiChatCompletions(requester.ProviderAPIRequester):
     """"""Google Gemini API 请求器""""""
 
     default_config: dict[str, typing.Any] = {